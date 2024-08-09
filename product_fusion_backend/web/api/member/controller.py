import secrets
from datetime import UTC, datetime, timedelta

from fastapi.encoders import jsonable_encoder
from starlette import status

from product_fusion_backend.core import VERIFY_EMAIL_WITH_PASS_RESET_TEMPLATE, APIResponse, StatusEnum, email_service
from product_fusion_backend.core.utils.hash_utils import hash_manager
from product_fusion_backend.dao import MemberDAO, OrganizationDAO, RoleDAO, UserDAO
from product_fusion_backend.web.api.member.schema import InviteMemberSchema


class OrganizationMemberService:
    @staticmethod
    async def invite_member(data: InviteMemberSchema, inviter_id: int) -> APIResponse:
        inviter_member = await MemberDAO().get_by_user_and_org(inviter_id, data.organization_id)  # type: ignore
        if not inviter_member or inviter_member.role.name not in ["admin", "owner"]:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="You don't have permission to invite members",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        org = await OrganizationDAO().get(data.organization_id)  # type: ignore
        if not org:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Organization not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        role = await RoleDAO().get(data.role_id)  # type: ignore
        if not role or role.org_id != data.organization_id:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Invalid role for the organization",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = await UserDAO().get_by_email(data.email)  # type: ignore
        if not user:
            user = await UserDAO().create(  # type: ignore
                {
                    "email": data.email,
                    "password": secrets.token_urlsafe(16),
                    "status": 0,
                },
            )

        existing_member = await MemberDAO().get_by_user_and_org(user.id, data.organization_id)  # type: ignore
        if existing_member:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="User is already a member of this organization",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        invite_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(days=7)

        await MemberDAO().create(  # type: ignore
            {
                "user_id": user.id,
                "org_id": data.organization_id,
                "role_id": data.role_id,
                "status": 0,
                "settings": {"invite_token": {"token": invite_token, "expires_at": expires_at.timestamp()}},
            },
        )

        invite_link = f"http://0.0.0.0:8000/api/org/member/accept-invite?token={invite_token}"
        await email_service.send_email(
            data.email,
            "Invitation to join organization",
            f"You've been invited to join an organization. Click here to accept: {invite_link}",
        )

        return APIResponse(
            status_=StatusEnum.SUCCESS,
            message="Invitation sent successfully",
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def accept_invite(token: str) -> APIResponse:
        member = await MemberDAO().get_by_invite_token(token)  # type: ignore
        if not member:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Invalid or expired invite token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        token_data = member.settings.get("invite_token", {})
        if datetime.now(UTC).timestamp() > token_data.get("expires_at", 0):
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Invite token has expired",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        await MemberDAO().update(  # type: ignore
            member.id,
            {
                "status": 1,
                "settings": {k: v for k, v in member.settings.items() if k != "invite_token"},  # Remove invite token
            },
        )

        verification_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(hours=24)

        user = await UserDAO().get(member.user_id)  # type: ignore
        _password = ""
        if user:
            user.settings = user.settings or {}
            user.settings["email_verification"] = {
                "token": verification_token,
                "expires_at": expires_at.timestamp(),
            }
            _password = user.password
            await UserDAO().update(  # type: ignore
                user.id,
                {
                    "settings": user.settings,  # type: ignore
                    "password": hash_manager.hash_password(user.password),  # type: ignore
                },
            )
            verification_link = f"http://0.0.0.0:8000/api/auth/verify-email?token={verification_token}"

            await email_service.send_email(
                user.email,
                "Verify Your Email and Set Password",
                VERIFY_EMAIL_WITH_PASS_RESET_TEMPLATE.format(verification_link, _password),
            )

        return APIResponse(
            status_=StatusEnum.SUCCESS,
            message="Invite accepted successfully! Please verify your email and set a password",
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def delete_member(member_id: int, org_id: int, deleter_id: int) -> APIResponse:
        deleter_member = await MemberDAO().get_by_user_and_org(deleter_id, org_id)  # type: ignore
        if not deleter_member or deleter_member.role.name not in ["admin", "owner"]:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="You don't have permission to delete members",
                status_code=403,
            )

        member = await MemberDAO().get_user_with_role(member_id)  # type: ignore
        if not member or member.org_id != org_id:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Member not found in the organization",
                status_code=404,
            )

        if member.role.name == "owner":
            owners_count = await MemberDAO().count_by_role_in_org("owner", org_id)  # type: ignore
            if owners_count <= 1:
                return APIResponse(
                    status_=StatusEnum.ERROR,
                    message="Cannot delete the last owner",
                    status_code=403,
                )

        await MemberDAO().delete(member_id)  # type: ignore

        return APIResponse(
            status_=StatusEnum.SUCCESS,
            message="Member deleted successfully",
            status_code=200,
        )

    @staticmethod
    async def update_member_role(member_id: int, org_id: int, new_role_id: int, updater_id: int) -> APIResponse:
        updater_member = await MemberDAO().get_by_user_and_org(updater_id, org_id)  # type: ignore
        if not updater_member or updater_member.role.name not in ["admin", "owner"]:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="You don't have permission to update member roles",
                status_code=403,
            )

        member = await MemberDAO().get_user_with_role(member_id)  # type: ignore
        if not member or member.org_id != org_id:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Member not found in the organization. Please invite the user first",
                status_code=404,
            )

        new_role = await RoleDAO().get(new_role_id)  # type: ignore
        if not new_role or new_role.org_id != org_id:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Invalid role for the organization",
                status_code=400,
            )

        # Prevent changing the role of the last owner
        if member.role.name == "owner":
            owners_count = await MemberDAO().count_by_role_in_org("owner", org_id)  # type: ignore
            if owners_count <= 1 and new_role.name != "owner":
                return APIResponse(
                    status_=StatusEnum.ERROR,
                    message="Cannot change the role of the last owner",
                    status_code=403,
                )

        updated_member = await MemberDAO().update(member_id, {"role_id": new_role_id})  # type: ignore
        updated_member_dict = updated_member.__dict__
        updated_member_dict.pop("_sa_instance_state")
        return APIResponse(
            status_=StatusEnum.SUCCESS,
            message="Member role updated successfully",
            data={
                "updated_member": jsonable_encoder(updated_member_dict),
            },
            status_code=200,
        )

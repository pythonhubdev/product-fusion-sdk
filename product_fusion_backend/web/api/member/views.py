from fastapi import APIRouter, Query, Request

from product_fusion_backend.core import APIResponse
from product_fusion_backend.web.api.member.controller import OrganizationMemberController
from product_fusion_backend.web.api.member.schema import DeleteMemberSchema, InviteMemberSchema, UpdateMemberRoleSchema

org_member_router = APIRouter(prefix="/org/member", tags=["Organization"])


@org_member_router.post("/invite")
async def invite_member(request: Request, data: InviteMemberSchema) -> APIResponse:
    inviter_id = request.state.user_id
    return await OrganizationMemberController.invite_member(data, inviter_id)


@org_member_router.get("/accept-invite")
async def accept_invite(token: str = Query(...)) -> APIResponse:
    return await OrganizationMemberController.accept_invite(token)


@org_member_router.delete("/delete")
async def delete_member(
    body: DeleteMemberSchema,
    request: Request,
) -> APIResponse:
    deleter_id = request.state.user_id
    return await OrganizationMemberController.delete_member(
        body.member_id,
        body.organization_id,
        deleter_id,
    )


@org_member_router.put("/update-role")
async def update_member_role(
    body: UpdateMemberRoleSchema,
    request: Request,
) -> APIResponse:
    updater_id = request.state.user_id
    return await OrganizationMemberController.update_member_role(
        body.member_id,
        body.organization_id,
        body.new_role_id,
        updater_id,
    )

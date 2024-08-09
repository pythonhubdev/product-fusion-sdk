from pydantic import BaseModel, EmailStr


class InviteMemberSchema(BaseModel):
    email: EmailStr
    organization_id: int
    role_id: int


class DeleteMemberSchema(BaseModel):
    member_id: int
    organization_id: int


class UpdateMemberRoleSchema(BaseModel):
    member_id: int
    organization_id: int
    new_role_id: int

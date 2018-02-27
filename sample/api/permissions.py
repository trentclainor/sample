from rest_framework.permissions import BasePermission


class ValidParentPKPermission(BasePermission):
    def has_permission(self, request, view):
        return view.is_valid_parent_pk()


class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_recruiter


class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_candidate

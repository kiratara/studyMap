from rest_framework import permissions


class UpdateSelfOnly(permissions.BasePermission):
    """Check user to allow/disallow changes to their information"""

    def has_object_permission(self, request, view, obj):
        """ 
        Check if user is attempting to access/update their own info.
        User's can only update their own user info.
        """
        if request.method in permissions.SAFE_METHODS: # safe methods include GET, method that do not require permission
            return True
        
        # checking if the user that requested the update and the 
        # user whose info is being attempted to be updated are same 
        # by comparing their id.
        return obj.id == request.user.id 

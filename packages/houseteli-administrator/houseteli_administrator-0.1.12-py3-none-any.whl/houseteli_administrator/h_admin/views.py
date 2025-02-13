from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Identity
from .serializers import IdentitySerializer
from django.db.models import Q

class IdentityView(APIView):
    """
    Read-only API for Identity. Returns the single Identity instance.
    Supports dynamic filtering based on query parameters.
    """

    def get(self, request):
        query_filters = Q()

        for key, value in request.query_params.items():
            if key in [field.name for field in Identity._meta.fields]:  # Ensure valid field
                field = Identity._meta.get_field(key)
                if field.is_relation:
                    related_model = field.related_model
                    if hasattr(related_model, "name"):  # Assume the related model has a 'name' field
                        key = f"{key}__name"

                query_filters &= Q(**{key: value})
        
        identity = Identity.objects.filter(query_filters).first()

        if identity:
            serializer = IdentitySerializer(identity)
            return Response(serializer.data)

        return Response({"error": "Identity not found"}, status=status.HTTP_404_NOT_FOUND)

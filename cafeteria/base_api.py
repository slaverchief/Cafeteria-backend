from rest_framework.response import Response
from rest_framework.views import APIView

class BaseCafeteriaApiView(APIView):
    Serializer = None
    Model = None

    def get_objects(self, request):
        return self.Model.objects.filter(**request.data)

    def get(self, request):
        serializers = self.Serializer(self.get_objects(request), many=True)
        return Response(serializers.data)

    def post(self, request):
        serializer = self.Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({"id": obj.id})

    def delete(self, request):
        self.Model.objects.get(**request.data).delete()
        return Response()
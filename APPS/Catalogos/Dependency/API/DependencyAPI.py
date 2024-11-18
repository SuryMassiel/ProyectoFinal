from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes

from rest_framework.permissions import IsAuthenticated

from APPS.Utils.PermisionAPI import CustomPermission
#IsAuthenticated: solo los usuarios logeados en el panel administrativo
#IsAdminUser: solo usuarios administradores
#IsAuthenticatedOrReadOnly: Solo los usuarios autenticados podran usar el CDU el resto solo Lectura
#EXISTEN OTROS Y CRAR NUEVOS PERMISOS PROPIOS
#AllowAny: para indicar que es un endpoint libre sin authenticar
from APPS.Utils.ResponseData import ResponseData


from APPS.Catalogos.Dependency.API.Serializer import DependencySerializer
from APPS.Catalogos.Dependency.models import Dependency


class DependencyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermission]  # [IsAdminOrReadOnly]
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

    def list(self, request):

        active_dependency = Dependency.objects.filter(Active=True)
        serializer = DependencySerializer(active_dependency, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTRO DE DEPENDENCIAS ACTIVAS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            dep = Dependency.objects.get(pk=pk)
            serializer = DependencySerializer(dep)

            data = ResponseData(
            Success= True,
            Status = status.HTTP_200_OK,
            Message='BUSQUEDA DE UNA DEPENDECIA EN PARTICULAR',
            Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Dependency.DoesNotExist:

            data = ResponseData(
            Success= False,
            Status = status.HTTP_404_NOT_FOUND,
            Message='NO EXISTE EL ID INGRESADO',
            Record = None
            )
            return Response (status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = DependencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nombre_existe = Dependency.objects.filter(CodeDependency=serializer.validated_data['CodeDependency']).exists()
        codigo_existe = Dependency.objects.filter(NameDependency=serializer.validated_data['NameDependency']).exists()

        if nombre_existe or codigo_existe:
            data = ResponseData(
                Success= False,
                Status = status.HTTP_400_BAD_REQUEST,
                Message='EL REGISTRO YA EXISTE',
                Record = None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        serializer.save()
        data = ResponseData(
            Success=True,
            Status = status.HTTP_201_CREATED,
            Message='REGISTRAR DEPENDENCIA',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def destroy(self, request, pk: int):
        try:
            dep = Dependency.objects.get(pk=pk)

            if not dep.Active:
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message='EL REGISTRO YA SE ENCUENTRA INACTIVO',
                    Record=None
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # marcar como inactivo
            dep.Active = False
            dep.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='SE MARCÓ COMO INACTIVO DE FORMA EXITOSA',
                Record= None
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Dependency.DoesNotExist:
            data =  ResponseData(
            Success=False,
            Status = status.HTTP_204_NO_CONTENT,
            Message='NO EXISTE EL REGISTRO A ANULAR',
            Record=None
            )
            return Response (status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    def update(self, request, pk: int):
        try:
            dep = Dependency.objects.get(pk=pk)
            serializer = DependencySerializer(instance=dep, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = ResponseData(
                Success= True,
                Status = status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Dependency.DoesNotExist:
            data = ResponseData(
                Success= False,
                Status = status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record = None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    @action(methods=['get'], detail=False)
    def list_inactive(self, request):

        inactive_dependency = Dependency.objects.filter(Active=False)
        serializer = DependencySerializer(inactive_dependency, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE DEPENDENCIAS INACTIVAS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())
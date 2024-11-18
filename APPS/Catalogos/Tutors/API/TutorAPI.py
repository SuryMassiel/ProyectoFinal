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
from APPS.Catalogos.Tutors.API.Serializer import TutorsSerializer
from APPS.Catalogos.Tutors.models import Tutors


class TutorsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermission]  # [IsAdminOrReadOnly]
    queryset = Tutors.objects.all()
    serializer_class = TutorsSerializer

    def list(self, request):

        active_tutors = Tutors.objects.filter(Active=True)
        serializer = TutorsSerializer(active_tutors, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTRO DE TUTORES ACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            tut = Tutors.objects.get(pk=pk)
            serializer = TutorsSerializer(tut)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSQUEDA DE UN TUTOR EN PARTICULAR',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Tutors.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND, ##Que no se encontró
                Message='NO EXISTE EL ID INGRESADO',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = TutorsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Tutors.objects.filter(CodeTutor=serializer.validated_data['CodeTutor']).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='EL CODIGO YA EXISTE',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        if Tutors.objects.filter(IdPerson=serializer.validated_data['IdPerson']).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='YA EXISTE UN REGISTRO DE ESTE TUTOR',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        serializer.save()
        data = ResponseData(
            Success=True,
            Status = status.HTTP_201_CREATED,
            Message='REGISTRAR TUTORS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def update(self, request, pk: int):
        try:
            tutor = Tutors.objects.get(pk=pk)
            serializer = TutorsSerializer(instance=tutor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = ResponseData(
                Success= True,
                Status = status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Tutors.DoesNotExist:
            data = ResponseData(
                Success= False,
                Status = status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record = None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def destroy(self, request, pk: int):
        try:
            tut = Tutors.objects.get(pk=pk)

            if not tut.Active:
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message='EL REGISTRO YA SE ENCUENTRA INACTIVO',
                    Record=None
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # marcar como inactivo
            tut.Active = False
            tut.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='SE MARCÓ COMO INACTIVO DE FORMA EXITOSA',
                Record=None
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())  # Respuesta con contenido

        except Tutors.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ANULAR',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

###################################################################################################

    @action(methods=['get'], detail=False)
    def filter_by_Occupation(self, request):
        ocupacion = request.query_params.get('Ocupacion')
        if not ocupacion:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='REVISAR SI EL CAMPO ESTA COMPLETO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        tutor = Tutors.objects.filter(Occupation=ocupacion)
        serializer = TutorsSerializer(tutor, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="FILTRACION POR OCUPACION",
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    @action(methods=['get'], detail=False)
    def list_inactive(self, request):

        inactive_tutors = Tutors.objects.filter(Active=False)
        serializer = TutorsSerializer(inactive_tutors, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE LOS TUTORES INACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())




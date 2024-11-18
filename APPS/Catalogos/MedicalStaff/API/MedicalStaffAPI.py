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

from APPS.Movimientos.MedicalHistory.models import MedicalHistory
from APPS.Catalogos.MedicalStaff.API.Serializer import MedicalStaffSerializer
from APPS.Catalogos.MedicalStaff.models import MedicalStaff

class MedicalStaffViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermission]  # [IsAdminOrReadOnly]
    queryset = MedicalStaff.objects.all()
    serializer_class = MedicalStaffSerializer

    def list(self, request):

        active_medicalStaff = MedicalStaff.objects.filter(Active=True)
        serializer = MedicalStaffSerializer(active_medicalStaff, many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DEL PERSONAL MEDICO ACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            per = MedicalStaff.objects.get(pk=pk)
            serializer = MedicalStaffSerializer(per)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSQUEDA DE UN PERSONAL EN PARTICULAR',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except MedicalStaff.DoesNotExist:

            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND, ##Que no se encontró
                Message='NO EXISTE EL ID INGRESADO',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = MedicalStaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if MedicalStaff.objects.filter(CodeMedicalStaff=serializer.validated_data['CodeMedicalStaff']).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='EL CODIGO YA EXISTE',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        if MedicalStaff.objects.filter(IdPerson=serializer.validated_data['IdPerson']).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='YA EXISTE UN REGISTRO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        serializer.save()
        data = ResponseData(
            Success=True,
            Status = status.HTTP_201_CREATED,
            Message='REGISTRAR PERSONAL MEDICO',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def update(self, request, pk: int):
        try:
            medstaff = MedicalStaff.objects.get(pk=pk)
            serializer = MedicalStaffSerializer(instance=medstaff, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = ResponseData(
                Success= True,
                Status = status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except MedicalStaff.DoesNotExist:
            data = ResponseData(
                Success= False,
                Status = status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record = None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def destroy (self, request, pk: int):
        try:
            medstaff = MedicalStaff.objects.get(pk=pk)

            if not medstaff.Active:
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message='EL REGISTRO YA SE ENCUENTRA INACTIVO',
                    Record=None
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # marcar como inactivo
            medstaff.Active = False
            medstaff.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='SE MARCÓ COMO INACTIVO DE FORMA EXITOSA',
                Record= None
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except MedicalStaff.DoesNotExist:
            data =  ResponseData(
            Success=False,
            Status = status.HTTP_204_NO_CONTENT,
            Message='NO EXISTE EL REGISTRO A ANULAR',
            Record=None
            )
            return Response (status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    @action(methods=['get'], detail=False)
    def list_inactive(self, request):

        inactive_medicalStaff = MedicalStaff.objects.filter(Active=False)
        serializer = MedicalStaffSerializer(inactive_medicalStaff, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE PERSONAL MEDICO INACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())


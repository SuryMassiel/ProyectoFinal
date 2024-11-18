from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes

from rest_framework.permissions import IsAuthenticated
#IsAuthenticated: solo los usuarios logeados en el panel administrativo
#IsAdminUser: solo usuarios administradores
#IsAuthenticatedOrReadOnly: Solo los usuarios autenticados podran usar el CDU el resto solo Lectura
#EXISTEN OTROS Y CRAR NUEVOS PERMISOS PROPIOS
#AllowAny: para indicar que es un endpoint libre sin authenticar
from APPS.Utils.PermisionAPI import CustomPermission
#importacion para responsedata
from APPS.Utils.ResponseData import ResponseData

from APPS.Movimientos.PediatricAppointment.models import PediatricAppointment
from APPS.Catalogos.Patients.API.Serializer import PatientsSerializer
from APPS.Catalogos.Patients.models import Patients


class PatientsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermission]
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer


    def list(self, request):

        active_patients = Patients.objects.filter(Active=True)
        serializer = PatientsSerializer(active_patients, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE PACIENTES ACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            pat = Patients.objects.get(pk=pk)
            serializer = PatientsSerializer(pat)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSQUEDA DE UN PACIENTE EN PARTICULAR',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Patients.DoesNotExist:

            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL ID INGRESADO',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = PatientsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Patients.objects.filter(CodePatient=serializer.validated_data['CodePatient']).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='EL CODIGO YA EXISTE',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Validar que registro de person no se haya utilizado
        if Patients.objects.filter(IdPerson=serializer.validated_data['IdPerson']).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='YA EXISTE UN REGISTRO DE ESTE PACIENTE',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        serializer.save()
        data = ResponseData(
            Success=True,
            Status = status.HTTP_201_CREATED,
            Message='REGISTRAR PACIENTE',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def update(self, request, pk: int):
        try:
            pat = Patients.objects.get(pk=pk)
            serializer = PatientsSerializer(instance=pat, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Patients.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def destroy (self, request, pk: int):
        try:
            patients = Patients.objects.get(pk=pk)

            if not patients.Active:
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message='EL REGISTRO YA SE ENCUENTRA INACTIVO',
                    Record=None
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # marcar como inactivo
            patients.Active = False
            patients.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='SE MARCÓ COMO INACTIVO DE FORMA EXITOSA',
                Record= None
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Patients.DoesNotExist:
            data =  ResponseData(
            Success=False,
            Status = status.HTTP_204_NO_CONTENT,
            Message='NO EXISTE EL REGISTRO A ANULAR',
            Record=None
            )
            return Response (status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

###################################################################################################

    # 1 CONTAR A LOS PACIENTES QUE TENGAN LAS MISMAS ALERGIAS
    @action(methods=['post'], detail=False)
    def Post_Count_by_Allergies(self, request):
        alergias = request.data.get("Alergias")

        if not alergias:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='REVISAR SI EL CAMPO ESTA COMPLETO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        cantidad_allergies = Patients.objects.filter(Allergies=alergias).count()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=f"CANTIDAD DE PACIENTES ALERGICOS A {alergias}",
            Record={'Cantidad': cantidad_allergies}
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

        # 2 LISTAR PACIENTES CON LA MISMA ALLERGIA

    @action(methods=['get'], detail=False)
    def Get_List_Patients_by_Allergy(self, request):
        alergia = request.query_params.get("Alergia")

        if not alergia:
            data = ResponseData(
                Success=True,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='REVISAR SI EL CAMPO ESTA COMPLETO',
                Record= None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        alergia_pacientes = Patients.objects.filter(Allergies=alergia)
        serializer = PatientsSerializer(alergia_pacientes, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="PACIENTES QUE POSEEN LA MISMA ALERGIA",
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    @action(methods=['get'], detail=False)
    def list_inactive(self, request):

        inactive_patients = Patients.objects.filter(Active=False)
        serializer = PatientsSerializer(inactive_patients, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE PACIENTES INACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())






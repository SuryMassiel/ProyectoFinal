from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes

from rest_framework.permissions import IsAuthenticated

from APPS.Catalogos.Patients.API.Serializer import PatientsSerializer
from APPS.Utils.PermisionAPI import CustomPermission
#IsAuthenticated: solo los usuarios logeados en el panel administrativo
#IsAdminUser: solo usuarios administradores
#IsAuthenticatedOrReadOnly: Solo los usuarios autenticados podran usar el CDU el resto solo Lectura
#EXISTEN OTROS Y CRAR NUEVOS PERMISOS PROPIOS
#AllowAny: para indicar que es un endpoint libre sin authenticar

from APPS.Utils.ResponseData import ResponseData

from APPS.Movimientos.MedicalHistory.API.Serializer import MedicalHistorySerializer
from APPS.Movimientos.MedicalHistory.models import MedicalHistory
from APPS.Catalogos.MedicalStaff.models import MedicalStaff
from APPS.Catalogos.Patients.models import Patients

class MedicalHistoryViewSet(ModelViewSet):
    permission_classes =[IsAuthenticated, CustomPermission] #[IsAdminOrReadOnly]
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer

    def list(self, request):

        active_medicalHistory = MedicalHistory.objects.filter(Active=True)
        serializer = MedicalHistorySerializer(active_medicalHistory, many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS HISTORIALES MEDICOS ACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            med = MedicalHistory.objects.get(pk=pk)
            serializer = MedicalHistorySerializer(med)

            data = ResponseData(
            Success= True,
            Status = status.HTTP_200_OK,
            Message='BUSQUEDA DE UN HISTORIAL MEDICO EN PARTICULAR',
            Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except MedicalHistory.DoesNotExist:
            data = ResponseData(
            Success= False,
            Status = status.HTTP_404_NOT_FOUND,
            Message='NO EXISTE EL ID INGRESADO',
            Record = None
            )
            return Response (status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = MedicalHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if MedicalHistory.objects.filter(CodeMedicalHistory=serializer.validated_data['CodeMedicalHistory']).exists():

            data = ResponseData(
                Success= False,
                Status = status.HTTP_400_BAD_REQUEST,
                Message='EL CODIGO YA EXISTE',
                Record = None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        serializer.save()
        data = ResponseData(
            Success=True,
            Status = status.HTTP_201_CREATED,
            Message='REGISTRAR HISTORIAL MEDICO',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def update(self, request, pk: int):
        try:
            med = MedicalHistory.objects.get(pk=pk)
            serializer = MedicalHistorySerializer(instance=med, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = ResponseData(
                Success= True,
                Status = status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())


        except MedicalHistory.DoesNotExist:
            data = ResponseData(
                Success= False,
                Status = status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record = None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

###################################################################################################

    #  1 CONTAR CUANTO HISTORIAL MEDICO  HAY EN LA BASE DE DATOSs

    @action(methods=['get'], detail=False)
    def Get_Count_MedicalHistory(self, request):
        cat_recod = MedicalHistory.objects.count()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='CANTIDAD DE HISTORIALES MEDICOS REGISTRADOS EN EL SISTEMA',
            Record={
                'Cantidad': cat_recod
            }
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    #2 POST BUSCAR HISTORIAL MEDICO POR "FECHA"
    @action(methods=['post'], detail=False)
    def Post_search_by_Date(self, request):
        fecha = request.data.get('Fecha')
        if not fecha:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,  # No procesa la solicitud debido a un error del usuraio/cliente
                Message='EL CAMPO "FECHA" ES OBLIGATORIO PARA REALIZAR LA BUSQUEDA',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        record = MedicalHistory.objects.filter(Date=fecha)

        if record.exists():
            serializer = MedicalHistorySerializer(record, many=True)

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSQUEDA DE HISTORIAL MEDICO',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,  # No procesa la solicitud debido a un error del usuraio/cliente
                Message='EL HISTORIAL MEDICO NO SE HA ENCONTRADO',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

#Reporte
    @action(methods=['get'], detail=False)
    def find_medicalhistory_by_date_range(self, request):
        fecha_inicio = request.query_params.get('FechaInicio')
        fecha_fin = request.query_params.get('FechaFin')
        paciente = request.query_params.get('IdPaciente')

        if not (fecha_inicio and fecha_fin):
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Los campos "Fecha Inicio" y "Fecha Fin" son obligatorios para realizar la búsqueda',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Validación del paciente
        if paciente:
            if not Patients.objects.filter(id=paciente).exists():
                return Response({
                    "Success": False,
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "El paciente especificado no existe",
                    "Record": None
                }, status=status.HTTP_404_NOT_FOUND)

        # Construcción del filtro dinámico
        filtro = {"Date__range": [fecha_inicio, fecha_fin]}
        if paciente:
            filtro["IdPatients"] = paciente

        # Consulta a la base de datos
        historial = MedicalHistory.objects.filter(**filtro)

        if historial.exists():
            serializer = MedicalHistorySerializer(historial, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Búsqueda del historial médico por fecha y paciente',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='No se encontro ningun registro de historial médico con los criterios proporcionados',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())
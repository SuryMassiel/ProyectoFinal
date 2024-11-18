from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes

from datetime import datetime, timezone
from rest_framework.permissions import IsAuthenticated

from APPS.Utils.PermisionAPI import CustomPermission
#IsAuthenticated: solo los usuarios logeados en el panel administrativo
#IsAdminUser: solo usuarios administradores
#IsAuthenticatedOrReadOnly: Solo los usuarios autenticados podran usar el CDU el resto solo Lectura
#EXISTEN OTROS Y CRAR NUEVOS PERMISOS PROPIOS
#AllowAny: para indicar que es un endpoint libre sin authenticar

from APPS.Utils.ResponseData import ResponseData

from APPS.Movimientos.PediatricAppointment.API.Serializer import PediatricAppointmentSerializer
from APPS.Movimientos.PediatricAppointment.models import PediatricAppointment
from APPS.Catalogos.MedicalStaff.models import MedicalStaff
from APPS.Catalogos.Patients.models import Patients

class PediatricAppointmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermission]  # [IsAdminOrReadOnly]
    queryset = PediatricAppointment.objects.all()
    serializer_class= PediatricAppointmentSerializer

    def list(self, request):

        active_appointment = PediatricAppointment.objects.filter(Active=True)
        serializer = PediatricAppointmentSerializer(active_appointment, many=True)
        data = ResponseData(
            Success= True,
            Status = status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE CITAS MEDICAS PEDIATRICAS ACTIVAS',
            Record = serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def update(self, request, pk: int):
        try:
            Cita = PediatricAppointment.objects.get(pk=pk)
            serializer = PediatricAppointmentSerializer(instance=Cita, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except PediatricAppointment.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            p = PediatricAppointment.objects.get(pk=pk)
            serializer = PediatricAppointmentSerializer(p)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSQUEDA DE CITA EN PARTICULAR',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except PediatricAppointment.DoesNotExist:

            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND, ##Que no se encontró
                Message='NO EXISTE EL ID INGRESADO',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = PediatricAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if PediatricAppointment.objects.filter(
                CodePediatricAppointment=serializer.validated_data['CodePediatricAppointment']).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='EL CODIGO YA EXISTE',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())


        paciente_id = request.data.get('IdPatients') or request.data.get('Paciente')
        paciente = Patients.objects.get(id=paciente_id)

        if not paciente.Active:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="NO SE PUEDE AGENDAR CITA, EL PACIENTE SE ENCUENTRA DESACTIVADO",
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())  # Se mueve dentro del if

        medico_id = request.data.get('MedicalStaffId') or request.data.get('Medico')
        medico = MedicalStaff.objects.get(id=medico_id)

        if not medico.Active:
            data = ResponseData(
                Success=False,  # Si el proceso no se ejecutó correctamente
                Status=status.HTTP_400_BAD_REQUEST,
                Message="NO SE PUEDE AGENDAR CITA, EL MEDICO SE ENCUENTRA DESACTIVADO",
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())  # Se mueve dentro del if

        medico_id = serializer.validated_data.get('MedicalStaffId')
        fecha_hora_cita = serializer.validated_data.get('DateTime')

        if fecha_hora_cita < datetime.now(timezone.utc):
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='LA FECHA Y HORA DE LA CITA NO PUEDEN SER EN EL PASADO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Validar que el médico no tenga otra cita en la misma fecha y hora
        if PediatricAppointment.objects.filter(MedicalStaffId=medico_id, DateTime=fecha_hora_cita).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='EL MÉDICO YA TIENE UNA CITA PROGRAMADA EN ESE MOMENTO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Guardar la cita si todas las validaciones pasan
        serializer.save()
        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='REGISTRAR CITA',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def destroy(self, request, pk: int):
        try:
            pac = PediatricAppointment.objects.get(pk=pk)

            if not pac.Active:
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message='EL REGISTRO YA SE ENCUENTRA INACTIVO',
                    Record=None
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # marcar como inactivo
            pac.Active = False
            pac.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='SE MARCÓ COMO INACTIVO DE FORMA EXITOSA',
                Record= None
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except PediatricAppointment.DoesNotExist:
            data =  ResponseData(
            Success=False,
            Status = status.HTTP_204_NO_CONTENT,
            Message='NO EXISTE EL REGISTRO A ANULAR',
            Record=None
            )
            return Response (status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

    ###################################################################################################

    # 1 POST BUSCAR CITA POR "CODIGO"

    @action(methods=['post'], detail=False)
    def search_by_Code(self, request):
        codigo = request.data.get('Codigo')
        if not codigo:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='REVISAR SI EL CAMPO ESTA COMPLETO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        citas = PediatricAppointment.objects.filter(CodePediatricAppointment__icontains=codigo)

        if citas.exists():
            serializer = PediatricAppointmentSerializer(citas, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message=f"BUSQUEDA DE CITA POR CODIGO",
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        else:

            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,  # No se encontro en el servidor
                Message='CITA MEDICA NO ENCONTRADA',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    #2 CONTAR CITAS DE LA BASE DE DATOS POST
    @action(methods=['get'], detail=False)
    def Get_Count_Appointments(self, request):
        cantCitas = PediatricAppointment.objects.count()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='CANTIDAD DE CITAS MEDICAS REGISTRADAS EN EL SISTEMA',
            Record={
                "CANTIDAD": cantCitas
            }
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    # 3 CONTAR CITAS QUE TENGAN EL MISMO ESTADO
    @action(methods=['post'], detail=False)
    def Post_Count_Appointments_By_State(self, request):
        estado = request.data.get("Estado")

        if not estado:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='REVISAR SI EL CAMPO ESTA COMPLETO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        cantidadCitas = PediatricAppointment.objects.filter(State=estado).count()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=f'CANTIDAD DE CITAS MEDICAS CON EL MISMO ESTADO ({estado}) EN EL SISTEMA',
            Record={
                "CANTIDAD": cantidadCitas
            }
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    # 4 LISTAR CITAS CON EL MISMO ESTADO
    @action(methods=['get'], detail=False)
    def Get_Appointments_by_State(self, request):
        estado = request.query_params.get("Estado")

        if not estado:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='REVISAR SI EL CAMPO ESTA COMPLETO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        estadoCita = PediatricAppointment.objects.filter(State=estado)
        serializer = PediatricAppointmentSerializer(estadoCita, many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=f"BUSQUEDA DE CITA POR ESTADO",
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    #5  POST BUSCAR CITAS POR "FECHA"
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

        citas = PediatricAppointment.objects.filter(DateTime__date=fecha)

        if citas.exists():
            serializer = PediatricAppointmentSerializer(citas, many=True)

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSQUEDA DE CITA MEDICA POR FECHA',
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

    @action(methods=['get'], detail=False)
    def list_inactive(self, request):

        inactive_pediatricAppointment = PediatricAppointment.objects.filter(Active=False)
        serializer = PediatricAppointmentSerializer(inactive_pediatricAppointment, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE LAS CITAS MEDICAS INACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    #Reporte
    @action(methods=['get'], detail=False)
    def find_appointments_by_date_range(self, request):
        fecha_inicio = request.query_params.get('FechaInicio')
        fecha_fin = request.query_params.get('FechaFin')
        medico = request.query_params.get('IdMedico')

        if not (fecha_inicio and fecha_fin):
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Los campos "Fecha Inicio" y "Fecha Fin" son obligatorios para realizar la búsqueda',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        # Validación del médico
        if medico:
            if not MedicalStaff.objects.filter(id=medico).exists():
                return Response({
                    "Success": False,
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "El médico especificado no existe",
                    "Record": None
                }, status=status.HTTP_404_NOT_FOUND)

        # Construcción del filtro dinámico
        filtro = {"DateTime__range": [fecha_inicio, fecha_fin]}
        if medico:
            filtro["MedicalStaffId"] = medico

        # Consulta a la base de datos
        citas = PediatricAppointment.objects.filter(**filtro)

        if citas.exists():
            serializer = PediatricAppointmentSerializer(citas, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Búsqueda de cita médica por fecha y médico',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())
        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='No se encontraron citas con los criterios proporcionados',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())
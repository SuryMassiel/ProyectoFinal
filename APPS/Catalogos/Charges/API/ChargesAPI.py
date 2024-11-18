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

from APPS.Catalogos.Charges.API.Serializer import ChargesSerializer
from APPS.Catalogos.Charges.models import Charges

class ChargesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermission]  # [IsAdminOrReadOnly]
    queryset = Charges.objects.all()
    serializer_class = ChargesSerializer

    def list(self, request):
        active_charger = Charges.objects.filter(Active=True)
        serializer = ChargesSerializer(active_charger, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTRO DE CARGOS ACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            charge = Charges.objects.get(pk=pk)
            serializer = ChargesSerializer(charge)

            data = ResponseData(
            Success= True,
            Status = status.HTTP_200_OK,
            Message='BUSQUEDA DE UN CARGO EN PARTICULAR',
            Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Charges.DoesNotExist:
            data = ResponseData(
            Success= False,
            Status = status.HTTP_404_NOT_FOUND,
            Message='NO EXISTE EL ID INGRESADO',
            Record = None
            )
            return Response (status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = ChargesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nombre_existe = Charges.objects.filter(NameCharges=serializer.validated_data['NameCharges']).exists()
        codigo_existe = Charges.objects.filter(CodeCharge=serializer.validated_data['CodeCharge']).exists()

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
            Message='REGISTRAR CARGO',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def destroy(self, request, pk: int):
        try:
            charg = Charges.objects.get(pk=pk)

            if not charg.Active:
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message='EL REGISTRO YA SE ENCUENTRA INACTIVO',
                    Record=None
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

            # marcar como inactivo
            charg.Active = False
            charg.save()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='SE MARCÓ COMO INACTIVO DE FORMA EXITOSA',
                Record=None
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Charges.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ANULAR',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def update(self, request, pk: int):
        try:
            charg = Charges.objects.get(pk=pk)
            serializer = ChargesSerializer(instance=charg, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = ResponseData(
                Success= True,
                Status = status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Charges.DoesNotExist:
            data = ResponseData(
                Success= False,
                Status = status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record = None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    @action(methods=['get'], detail=False)
    def list_inactive(self, request):

        inactive_charges = Charges.objects.filter(Active=False)
        serializer = ChargesSerializer(inactive_charges, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTROS DE CARGOS INACTIVOS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

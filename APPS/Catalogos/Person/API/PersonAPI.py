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
from APPS.Utils.ResponseData import ResponseData

from APPS.Catalogos.Person.API.Serializer import PersonSerializer
from APPS.Catalogos.Person.models import Person

class PersonViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]  # [IsAdminOrReadOnly]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def list(self, request):
        serializer = PersonSerializer(Person.objects.all(), many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='LISTADO DE LOS REGISTRO DE LAS PERSONAS',
            Record=serializer.data
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())

    def retrieve(self, request, pk: int):
        try:
            per = Person.objects.get(pk=pk)
            serializer = PersonSerializer(per)

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSQUEDA DE UNA PERSONA EN PARTICULAR',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Person.DoesNotExist:

            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,  ##Que no se encontró
                Message='NO EXISTE EL ID INGRESADO',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def create(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identificacion_existe = serializer.validated_data.get('IdentityCard')

        if identificacion_existe is not None:
            if Person.objects.filter(IdentityCard=identificacion_existe).exists():
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message='EL REGISTRO YA EXISTE',
                    Record=None
                )
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        serializer.save()
        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='REGISTRAR PERSONA',
            Record=serializer.data
        )
        return Response(status=status.HTTP_201_CREATED, data=data.toResponse())

    def update(self, request, pk: int):

        try:
            person = Person.objects.get(pk=pk)
            serializer = PersonSerializer(instance=person, data=request.data)
            serializer.is_valid(raise_exception= True)
            serializer.save()

            data = ResponseData(
                Success= True,
                Status = status.HTTP_200_OK,
                Message='REGISTRO ACTUALIZADO CORRECTAMENTE',
                Record = serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        except Person.DoesNotExist:
            data = ResponseData(
                Success= False,
                Status = status.HTTP_404_NOT_FOUND,
                Message='NO EXISTE EL REGISTRO A ACTUALIZAR',
                Record = None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())

    def destroy(self, request, pk: int):
        try:
            person = Person.objects.get(pk=pk)
            person.delete()

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='SE ELIMINO DE FORMA EXITOSA',
                Record=None
            )
            return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())  # Respuesta sin contenido

        except Person.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_204_NO_CONTENT,
                Message='NO EXISTE EL REGISTRO A ELIMINAR',
                Record=None
            )
            return Response(status=status.HTTP_204_NO_CONTENT, data=data.toResponse())

###################################################################################################

    # 1   POST BUSCAR PERSONA POR NOMBRE
    @action(methods=['post'], detail=False)
    def Post_search_by_first_name(self, request):
        nombre = request.data.get('Nombre')
        if not nombre:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,  # No procesa la solicitud debido a un error del usuraio/cliente
                Message='EL CAMPO "NOMBRE" ES OBLIGATORIO',
                Record=None
            )
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.toResponse())

        personas = Person.objects.filter(Firstname__icontains=nombre)
        if personas.exists():
            serializer = PersonSerializer(personas, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='BUSCAR PERSONA POR MEDIO DEL NOMBRE',
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=data.toResponse())

        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,  # No se encontro en el servidor
                Message='PERSONA NO ENCONTRADA',
                Record=None
            )
            return Response(status=status.HTTP_404_NOT_FOUND, data=data.toResponse())
    #2
    @action(methods=['get'], detail=False)
    def Get_count_by_gender(self, request):
        total_hombres = Person.objects.filter(Sexo='Masculino').count()
        total_mujeres = Person.objects.filter(Sexo='Femenino').count()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='CONTEO POR GENERO',
            Record={
                "Hombres": total_hombres,
                "Mujeres": total_mujeres
            }
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())
    #3
    @action(methods=['get'], detail=False)
    def Get_Contar_Person(self, request):
        cant_pers = Person.objects.count()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='CANTIDAD DE PERSONAS REGISTRADAS EN LA BASE DE DATOS',
            Record={
                "CANTIDAD": cant_pers
            }
        )
        return Response(status=status.HTTP_200_OK, data=data.toResponse())






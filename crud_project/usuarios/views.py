from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope
import requests

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_usuario(request):
    data = request.data
    tipo_usuario = data.get('tipo')

    if tipo_usuario == 'comprador':
        if not data.get('direccion'):
            return Response({'error': settings.ERROR_MESSAGES['ERROR_DIRECCION_COMPRADOR']}, status=status.HTTP_400_BAD_REQUEST)
        if data.get('cargo'):
            data['cargo'] = None

    elif tipo_usuario == 'vendedor':
        if data.get('direccion'):
            return Response({'error': settings.ERROR_MESSAGES['ERROR_DIRECCION_VENDEDOR']}, status=status.HTTP_400_BAD_REQUEST)
        elif not data.get('cargo'):
            return Response({'error': settings.ERROR_MESSAGES['ERROR_CARGO_VENDEDOR']}, status=status.HTTP_400_BAD_REQUEST)
        elif data.get('cargo') not in ['asesor', 'cajero']:
            return Response({'error': settings.ERROR_MESSAGES['ERROR_CARGO_INVALIDO']}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UsuarioSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, TokenHasReadWriteScope])
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, TokenHasReadWriteScope])
def obtener_usuario(request, id):
    try:
        usuario = Usuario.objects.get(pk=id)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, TokenHasReadWriteScope])
def eliminar_usuario(request, id):
    try:
        usuario = Usuario.objects.get(pk=id)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated, TokenHasReadWriteScope])
def geocodificar_base(request):
    api_key = settings.GOOGLE_GEOCODING_API_KEY
    compradores = Usuario.objects.filter(tipo='comprador', longitud__isnull=True, latitud__isnull=True)
    
    # Buscar compradores
    if not compradores.exists():
        return Response({'error': 'No hay compradores que cumplan con los criterios de filtro.'}, status=status.HTTP_404_NOT_FOUND)
    
    for comprador in compradores:
        direccion = comprador.direccion
        ciudad = comprador.ciudad
        full_address = f"{direccion}, {ciudad}"    
    
        try:
            response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': full_address, 'key': api_key})
            response.raise_for_status()  # Error en la solicitud
            geocode_data = response.json()
        except requests.exceptions.RequestException as e:
            print('Error en la solicitud a la API de Google:', e)
            return Response({'error': 'Error en la solicitud a la API de Google.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print('Datos de geocodificación de Google:', geocode_data)
        
        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            comprador.longitud = location['lng']
            comprador.latitud = location['lat']
            comprador.estado_geo = True
            print(f'Longitud y latitud actualizadas para {comprador.nombre}: {comprador.longitud}, {comprador.latitud}')
        else:
            comprador.longitud = 0
            comprador.latitud = 0
            print(f'No se pudo geocodificar la dirección para {comprador.nombre}.')
        
        comprador.save()
    
    # Exito en la solicitud
    return Response({'status': 'Geocodificación completada.'})


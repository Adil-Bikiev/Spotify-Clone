from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import requests
from decouple import config
import os, json
# Create your views here

def top_artists():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/artists/top"

    querystring = {"type":"weekly"}

    headers = {
        "x-rapidapi-key": f"{config('APIKEY')}",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()

    artists_info = []

    if 'artists' in response_data:
        for artist in response_data['artists']:
            name = artist.get('name', 'No Name')
            avatar_url = artist.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
            artist_id = artist.get('id', 'No ID')
            artists_info.append((name, avatar_url, artist_id))

    print(response.status_code)
    print(response.text)
    return artists_info 


def index(request):
    return render(request, 'SpotifyCloneApp/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('user_in')
        else:
            messages.info(request, 'Неправильные данные!')
            return redirect('login')

    return render(request, 'SpotifyCloneApp/login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Данный Email уже занят!')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Данный Username уже занят!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('user_in')
        else:
            messages.info(request, 'Пароли не совпадают!')
            return redirect('signup')
    else:
        return render(request, 'SpotifyCloneApp/signup.html')

@login_required(login_url='login')
def user_in(request):
    return render(request, 'SpotifyCloneApp/user_in.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def library_user(request):
    artists_info = top_artists()
    print(artists_info)
    context = {
        'artists_info': artists_info,
    }

    return render(request, 'SpotifyCloneApp/library.html', context)


def top_songs():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/tracks/top"

    querystring = {"type":"weekly"}

    headers = {
        "x-rapidapi-key": f"{config('APIKEY')}",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    track_details = []

    if 'tracks' in data:
        shortened_data = data['tracks'][:18]


        for track in shortened_data:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name'] if track['artists'] else None
            cover_url = track['album']['cover'][0]['url'] if track['album']['cover'] else None

            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url,
            })

    else:
        print('Track not found is response')

    return track_details

@login_required(login_url='login')
def top_tracks_view(request):
    tracks = top_songs()
    return render(request, 'SpotifyCloneApp/songs.html', {'tracks': tracks})

def get_audio(query):
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud"

    querystring = {"track": query }

    headers = {
        "x-rapidapi-key": f"{config('APIKEY')}",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    audio_details = []

    if response.status_code == 200:
        response_data = response.json()

        if "youtubeVideo" in response_data and 'audio' in response_data['youtubeVideo']:
            audio_list = response_data['youtubeVideo']['audio']
            if audio_list:
                first_audio_url = audio_list[0]['url']
                duration_text = audio_list[0]['durationText']

                audio_details.append(first_audio_url)
                audio_details.append(duration_text)
            else:
                print("Аудио не доступно!")
        else:
            print("Нет 'youtubeVideo' или 'audio'!")
    else:
        print("Проблема в данных!")
    return audio_details

@login_required(login_url='login')
def music(request, pk):

    track_id = pk
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/metadata"

    querystring = {"trackId": track_id}

    headers = {
        "x-rapidapi-key": f"{config('APIKEY')}",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()

        track_name = data.get("name")
        artists_list = data.get("artists", [])
        first_atrist_name = artists_list[0].get("name") if artists_list else "Музыканты не найдены"

        audio_details_query = track_name + first_atrist_name
        audio_details = get_audio(audio_details_query)
        audio_url = audio_details[0]
        duration_text = audio_details[1]

        context = {
            'track_name': track_name,
            'artist_name': first_atrist_name,
        }
    return render(request, 'music.html', context)

@login_required(login_url='login')
def profile(request, pk):
    artist_id = pk
    url = "https://spotify-scraper.p.rapidapi.com/v1/artist/overview"

    querystring = {"artistId": artist_id}

    headers = {
        "x-rapidapi-key": f"{config('APIKEY')}",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        name = data["name"]
        monthly_listeners = data["stats"]["monthlyListeners"]
        header_url = data["visuals"]["header"][0]["url"]

        artist_data = {
            "name": name,
            "monthlyListeners": monthly_listeners,
            "headerUrl": header_url,
        }
    else:
        artist_data = {}

    return render(request, 'profile.html')
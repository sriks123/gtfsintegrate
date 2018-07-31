import json
import os

import requests
from conversionapp.models import Correspondence, ExtraField, Correspondence_Route, Correspondence_Agency
from django.db import connection
from django.shortcuts import render
from gs.forms import Correspondence_Route_Form, Correspondence_Agency_Form
from gs.tasks import save_comp, connect_to_JOSM, get_itineraries
from multigtfs.models import Stop, Feed, Route
from osmapp.views import load
from requests import post

from .models import CMP_Stop
from .models import Relation_data

nodes_info = [['37008337', 'ref', '13'], ['1525729024', 'name', 'Southwest 6th & West Burnside', 'ref', '7751'],
              ['1525729024', 'name', 'Southwest 6th & West Burnside', 'ref', '7751'],
              ['1525729024', 'name', 'Southwest 6th & West Burnside', 'ref', '7751'],
              ['1525729024', 'name', 'Southwest 6th & West Burnside', 'ref', '7751'],
              ['1525737720', 'name', 'Southwest 5th & Pine', 'ref', '7631'],
              ['1525737720', 'name', 'Southwest 5th & Pine', 'ref', '7631'],
              ['1525737720', 'name', 'Southwest 5th & Pine', 'ref', '7631'],
              ['1525737720', 'name', 'Southwest 5th & Pine', 'ref', '7631'],
              ['1525749970', 'name', 'Southwest 5th & Washington', 'ref', '7642'],
              ['1525749970', 'name', 'Southwest 5th & Washington', 'ref', '7642'],
              ['1525749970', 'name', 'Southwest 5th & Washington', 'ref', '7642'],
              ['1525749970', 'name', 'Southwest 5th & Washington', 'ref', '7642'],
              ['1525749987', 'name', 'Southwest 6th & Stark', 'ref', '7797'],
              ['1525749987', 'name', 'Southwest 6th & Stark', 'ref', '7797'],
              ['1525749987', 'name', 'Southwest 6th & Stark', 'ref', '7797'],
              ['1525749987', 'name', 'Southwest 6th & Stark', 'ref', '7797'],
              ['1525749987', 'name', 'Southwest 6th & Stark', 'ref', '7797'],
              ['1525749987', 'name', 'Southwest 6th & Stark', 'ref', '7797'],
              ['1525760109', 'name', 'Southwest 5th & Salmon', 'ref', '7634'],
              ['1525760109', 'name', 'Southwest 5th & Salmon', 'ref', '7634'],
              ['1525760109', 'name', 'Southwest 5th & Salmon', 'ref', '7634'],
              ['1525760109', 'name', 'Southwest 5th & Salmon', 'ref', '7634'],
              ['1525760109', 'name', 'Southwest 5th & Salmon', 'ref', '7634'],
              ['1525760223', 'name', 'Southwest 6th & Taylor', 'ref', '7800'],
              ['1525760223', 'name', 'Southwest 6th & Taylor', 'ref', '7800'],
              ['1525760223', 'name', 'Southwest 6th & Taylor', 'ref', '7800'],
              ['1525760223', 'name', 'Southwest 6th & Taylor', 'ref', '7800'],
              ['1525760223', 'name', 'Southwest 6th & Taylor', 'ref', '7800'],
              ['1525820922', 'name', 'Southwest Madison & 1st', 'ref', '3635'],
              ['1525820922', 'name', 'Southwest Madison & 1st', 'ref', '3635'],
              ['1525820922', 'name', 'Southwest Madison & 1st', 'ref', '3635'],
              ['1525820922', 'name', 'Southwest Madison & 1st', 'ref', '3635'],
              ['1525820928', 'name', 'Southwest Madison & 4th', 'ref', '3639'],
              ['1525820928', 'name', 'Southwest Madison & 4th', 'ref', '3639'],
              ['1525820928', 'name', 'Southwest Madison & 4th', 'ref', '3639'],
              ['1525820928', 'name', 'Southwest Madison & 4th', 'ref', '3639'],
              ['1525820928', 'name', 'Southwest Madison & 4th', 'ref', '3639'],
              ['1525820928', 'name', 'Southwest Madison & 4th', 'ref', '3639'],
              ['1525825853', 'name', 'Southwest Main & 2nd', 'ref', '11956'],
              ['1525825853', 'name', 'Southwest Main & 2nd', 'ref', '11956'],
              ['1525825853', 'name', 'Southwest Main & 2nd', 'ref', '11956'],
              ['2681749539', 'name', 'Southeast Martin Luther King & Mill', 'ref', '5933'],
              ['2681749539', 'name', 'Southeast Martin Luther King & Mill', 'ref', '5933'],
              ['2681749539', 'name', 'Southeast Martin Luther King & Mill', 'ref', '5933'],
              ['2681749539', 'name', 'Southeast Martin Luther King & Mill', 'ref', '5933'],
              ['2681753018', 'name', 'Southeast Grand & Mill', 'ref', '2171'],
              ['2681753018', 'name', 'Southeast Grand & Mill', 'ref', '2171'],
              ['2681753018', 'name', 'Southeast Grand & Mill', 'ref', '2171'],
              ['2681753018', 'name', 'Southeast Grand & Mill', 'ref', '2171'],
              ['2681754930', 'name', 'Southeast McLoughlin & 17th', 'ref', '3859'],
              ['2681754930', 'name', 'Southeast McLoughlin & 17th', 'ref', '3859'],
              ['2681754930', 'name', 'Southeast McLoughlin & 17th', 'ref', '3859'],
              ['2681754930', 'name', 'Southeast McLoughlin & 17th', 'ref', '3859']]
relation_ids = [2688727]
relations_info = [['name', 'Southeast Grand & Mill', 'ref', '2171'],
                  ['name', 'Southeast McLoughlin & 17th', 'ref', '3859'],
                  ['ref', '13']]


def get_nodes_within100m(lon, loat):
    query = "SELECT * FROM osmapp_node WHERE ST_DWithin(geom, 'Point({0} {1})', 100)".format(lon, lat)  # lon, lat
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    return result


def showmap_with_comp(request, pk):
    context = {
        'type': 'conversion_view',
        'feed_id': pk,
        'feed_name': Feed.objects.get(id=pk).name,
        'error': 'No errors'
    }

    # 1. Load all stops first
    try:
        stops = Stop.objects.filter(feed=pk)
    except Exception as e:
        context['error'] = 'No stops present'

    # Initially comparison should be done by the user
    try:
        for stop in stops:
            # osm_nodes_in_bound = get_nodes_within100m(str(stop.lon),str(stop.lat))
            if not CMP_Stop.objects.filter(gtfs_stop=stop).exists():
                comp_stop = CMP_Stop.objects.create(gtfs_stop=stop)
                comp_stop.save()
    except Exception as e:
        context['error'] = e

    '''
    #to be executed if the matching needs to be done by the app
    for stop in stops:
        nodes = get_nodes_within100m(str(stop.lon),str(stop.lat))

        # create a cmp_stop data
        if CMP_Stop.objects.filter(gtfs_stop=stop).exists():
            comp_stop = CMP_Stop.objects.get(gtfs_stop=stop)
            if len(result) > 0:
                for osm_node_info in result:
                    osm_node = Node.objects.get(id=osm_node_info[0])
                    comp_stop.probable_matched_stops.add(osm_node)
                    comp_stop.save()
        else:
            comp_stop = CMP_Stop.objects.create(gtfs_stop=stop, matching_type='LOCATION')
            comp_stop.save()'''

    return render(request, 'gs/comparison.html', {'context': context})


def create_stop(request):
    if request.method == 'POST':
        data_json = request.POST.get('data_to_match')
        data = json.loads(data_json)
        feed_id = data[0]['feed_id']
        gtfs_stop_data = data[0]['gtfs']
        lat = data[0]['lat']
        lon = data[0]['lon']
        print(gtfs_stop_data)

        outputparams = {'newline': '', 'ident': '', 'generator': 'Python script', 'upload': True}

        xml = "<?xml version='1.0' encoding='UTF-8'?>{newline}<osm version='0.6'{upload}{generator}>{newline}".format(
            **outputparams)
        name = gtfs_stop_data['name'].replace('&', '&amp;').replace("'", "&apos;").replace("<", "&lt;").replace(">",
                                                                                                                "&gt;").replace(
            '"', "&quot;")
        xml += '''<nd action="modify" id='-1' timestamp='2013-04-23T05:33:57Z' uid='28923' user='testuser' visible='True' version='1' changeset='15832248' incomplete='False' feed_id='2' lon="''' + str(
            lon) + '''" lat="''' + str(
            lat) + '''" ><tag k='public_transport' v='platform' /><tag k='bus' v='yes' /><tag k='name' v="''' + \
               name + '''" /><tag k='ref' v="''' + str(
            gtfs_stop_data['stop_id']) + '''" /></node></osm></xml>'''
        values = {'data': xml, 'new_layer': True}
        link = "http://localhost:8111/add_node?lon=" + str(lon) + "&lat=" + str(lat) + "&addtags=name=" + \
               name + "|ref=" + str(gtfs_stop_data['stop_id'])
        response = requests.get(link)

        return render(request, 'gs/comparison.html')


def match_stop(request):
    if request.method == 'POST':
        context = {
            'match_success': 0,
            'error': ''
        }

        data_to_match_json = request.POST.get('data_to_match')
        data_to_match = json.loads(data_to_match_json)

        print(data_to_match)

        feed_id = data_to_match[0]['feed_id']
        gtfs_stop_data = data_to_match[0]['gtfs']
        osm_stop_data = data_to_match[0]['osm']

        generator = 'Python Script'
        outputparams = {
            'newline': '\n',
            'indent': ' ',
            'upload': '',
            'generator': " generator='{}'".format(generator)
        }

        xml = '''<?xml version='1.0' encoding='UTF-8' ?>{newline}<osm version='0.6'{upload}{generator}>{newline}'''.format(
            **outputparams)
        xml += save_comp(gtfs_stop_data, osm_stop_data, feed_id, stops_layer=False)
        xml += '''{newline}</osm>'''.format(**outputparams)
        connect_to_JOSM(xml)

        print(xml)

    return render(request, 'gs/comparison.html')


def match_stops(request):
    if request.method == 'POST':
        context = {
            'match_success': 0,
            'error': ''
        }
        data_to_match_json = request.POST.get('data_to_match')
        data_to_match = json.loads(data_to_match_json)

        print(data_to_match)

        generator = 'Python Script'
        outputparams = {
            'newline': '\n',
            'indent': ' ',
            'upload': '',
            'generator': " generator='{}'".format(generator)
        }
        xml = '''<?xml version='1.0' encoding='UTF-8' ?>{newline}<osm version='0.6'{upload}{generator}>{newline}'''.format(
            **outputparams)
        for i in range(0, len(data_to_match)):
            feed_id = data_to_match[i]['feed_id']
            gtfs_stop_data = data_to_match[i]['gtfs']
            osm_stop_data = data_to_match[i]['osm']
            xml += save_comp(gtfs_stop_data, osm_stop_data, feed_id, stops_layer=True)

        xml += '''{newline}</osm>'''.format(**outputparams)
        print(xml)
        connect_to_JOSM(xml)

        '''
        stops_layer = True
        data_in_string = request.POST.get('match_data')
        data_in_json = json.loads(data_in_string)
        tags_json = request.POST.get('tags')
        tags_data = json.loads(tags_json)
        print(tags_data)

        generator = 'Python Script'
        outputparams = {
            'newline': '\n',
            'indent': ' ',
            'upload': '',
            'generator': " generator='{}'".format(generator)
        }
        '''
        # xml = '''<?xml version='1.0' encoding='UTF-8' ?>{newline}<osm version='0.6'{upload}{generator}>{newline}'''.format(
        #    **outputparams)

        '''
        for i in range(0, len(data_in_json)):
            str = data_in_json[i]['gtfs_stop'].split('-')
            gtfs_feed_id = str[0]
            gtfs_stop_id = str[1]
            osm_stop_id = data_in_json[i]['osm_stop']

            xml += save_comp(gtfs_feed_id, gtfs_stop_id, osm_stop_id, tags_data[i], stops_layer)
        '''
        # xml += '''{newline}</osm>'''.format(**outputparams)
        # connect_to_JOSM(xml)

    return render(request, 'gs/comparison.html', {'context': context})


def define_relation(request, pk=None):
    if request.method == "POST":
        route_form = Correspondence_Route_Form(request.POST)

        if route_form.is_valid():
            entered_route_corr_form = route_form.save(commit=False)
            entered_route_corr_form_feed_id = entered_route_corr_form.feed_id

            if Correspondence_Route.objects.filter(feed_id=entered_route_corr_form_feed_id).exists():
                print("Saving Route form")
            else:
                entered_route_corr_form.save()
    else:
        corr_form = Correspondence.objects.get(feed_id=pk)
        print(corr_form)

        context = {
            'feed_id': pk,
            'extra_data': '',
            'extra_data_ex': ''
        }

        extra_field_keys = []
        extra_data_ex = {}
        feed_routes = Route.objects.filter(feed=pk)
        print(feed_routes.all()[0].extra_data)
        ExtraField.objects.filter(feed_id=pk).all().delete()
        for i in range(0, len(feed_routes)):
            extra_data = feed_routes[i].extra_data
            for key, value in extra_data.items():
                if key not in extra_field_keys:
                    extra_field_keys.append(key)
                    if ExtraField.objects.filter(feed_id=pk, field_name=key, value=None).exists():
                        ef = ExtraField.objects.filter(feed_id=pk, field_name=key, value=None)[0]
                    else:
                        ef = ExtraField(feed_id=pk, field_name=key)
                        ef.save()
        context['extra_field_ex'] = extra_data_ex
        context['extra_field_keys'] = extra_field_keys
        route_form = Correspondence_Route_Form()
        return render(request, 'gs/define-relation.html',
                      {'context': context, 'route_form': route_form})


def save_route_corr(request):
    if request.method == "POST":
        route_form = Correspondence_Route_Form(request.POST)
        entered_route_corr_form_feed_id = -1
        if route_form.is_valid():
            entered_route_corr_form = route_form.save(commit=False)
            entered_route_corr_form_feed_id = entered_route_corr_form.feed_id
            context = {
                'feed_id': entered_route_corr_form_feed_id
            }
            if Correspondence_Route.objects.filter(feed_id=entered_route_corr_form_feed_id).exists():
                route_corr_obj = Correspondence_Route.objects.get(feed_id=entered_route_corr_form_feed_id)
                route_corr_obj.route_id = entered_route_corr_form.route_id
                route_corr_obj.agency = entered_route_corr_form.agency
                route_corr_obj.short_name = entered_route_corr_form.short_name
                route_corr_obj.long_name = entered_route_corr_form.long_name
                route_corr_obj.desc = entered_route_corr_form.desc
                route_corr_obj.rtype = entered_route_corr_form.rtype
                route_corr_obj.url = entered_route_corr_form.url
                route_corr_obj.color = entered_route_corr_form.color
                route_corr_obj.text_color = entered_route_corr_form.text_color

                route_corr_obj.save()
            else:
                entered_route_corr_form.save()

        else:
            print("Route form not valid {}".format(route_form))

        agency_form = Correspondence_Agency_Form()
        return render(request, 'gs/define-relation.html', {'context': context, 'agency_form': agency_form})


def save_ag_corr(request):
    if request.method == "POST":
        context = {
            'feed_id': -1
        }
        agency_form = Correspondence_Agency_Form(request.POST)

        if agency_form.is_valid():
            entered_agency_corr_form = agency_form.save(commit=False)
            entered_agency_corr_form_feed_id = entered_agency_corr_form.feed_id

            if Correspondence_Agency.objects.filter(feed_id=entered_agency_corr_form_feed_id).exists():
                ag_corr_obj = Correspondence_Agency.objects.get(feed_id=entered_agency_corr_form_feed_id)
                ag_corr_obj.feed_id = entered_agency_corr_form_feed_id
                ag_corr_obj.agency_name = entered_agency_corr_form.agency_name
                ag_corr_obj.agency_id = entered_agency_corr_form.agency_id
                ag_corr_obj.agency_url = entered_agency_corr_form.agency_url
                ag_corr_obj.agency_timezone = entered_agency_corr_form.agency_timezone
                ag_corr_obj.agency_lang = entered_agency_corr_form.agency_lang
                ag_corr_obj.agency_phone = entered_agency_corr_form.agency_phone
                ag_corr_obj.agency_fare_url = entered_agency_corr_form.agency_fare_url

                ag_corr_obj.save()
            else:
                entered_agency_corr_form.save()

            '''Creating XML File'''
            # get the routes form with that feed
            routes_list = Route.objects.filter(feed=entered_agency_corr_form_feed_id)
            routes_form = Correspondence_Route.objects.get(feed_id=entered_agency_corr_form_feed_id)

            valid_routes_attr_list = {}
            long_names_list = []
            short_names_list = []
            route_ids_db = []
            routes_data = {}
            extra_data_present = False
            extra_data = routes_form.extra_data.all()
            form_extra_data = {}
            form_extra_data_values = []
            if extra_data.count() > 0:
                extra_data_present = True

            if extra_data_present:
                for key in extra_data:
                    form_extra_data.update({key.field_name: key.value})
            print(form_extra_data)
            for key, value in routes_form.__dict__.items():
                if key == '_state':
                    continue
                elif key == 'feed_id':
                    continue
                else:
                    if value != '':
                        pair = {key: value}
                        valid_routes_attr_list.update(pair)

            print(valid_routes_attr_list)
            xml = ''

            choices = {
                '0': 'Tram, Streetcar, or Light rail',
                '1': 'Subway or Metro',
                '2': 'rail',
                '3': 'bus',
                '4': 'ferry',
                '5': 'Cable Car',
                '6': 'Godola or Suspended cable car',
                '7': 'Funicular'
            }

            for route in routes_list:
                xml += "\n<tag k='type' v='route_master'>\n"
                build_route_data = {}
                for r_key, r_value in route.__dict__.items():

                    if r_key == 'id':
                        route_ids_db.append(r_value)
                    if r_key == 'long_name':
                        val = r_value.replace('"', '')
                        long_names_list.append(val)
                    elif r_key == 'short_name':
                        sval = r_value.replace('"', '')
                        short_names_list.append(sval)
                    elif r_key == 'extra_data':
                        extra_data_json = r_value

                        if extra_data_present:
                            for ekey, evalue in extra_data_json.items():
                                xml += "<tag k='" + str(form_extra_data[ekey]) + "' v='" + str(evalue) + "' />\n"

                    if r_key in valid_routes_attr_list:
                        tag_key = valid_routes_attr_list[r_key]
                        if tag_key == 'colour' or tag_key == 'text_colour':
                            tag_val = '#' + r_value
                        elif r_key == 'rtype':
                            tag_val = choices[str(r_value)]
                        else:
                            tag_val = r_value

                        if tag_val != '' and str(tag_key) != 'None' and r_key != 'id':
                            xml += "<tag k='" + str(tag_key) + "' v='" + str(tag_val) + "' />\n"

            print(xml)
            complete_data = []

            if '' in long_names_list:
                if '' in short_names_list:
                    for i in range(0, long_names_list):
                        long_names_list[i] = 'line ' + str(i)
                else:
                    long_names_list = short_names_list

            print(long_names_list)

            for (route_id, name) in zip(route_ids_db, long_names_list):
                data = {"id": route_id, "name": name}
                routes_data[route_id] = name

            for i in range(0, len(route_ids_db)):
                if i == 0:
                    complete_data.append(get_itineraries(route_ids_db[i], entered_agency_corr_form_feed_id, start=True))
                else:
                    complete_data.append(
                        get_itineraries(route_ids_db[i], entered_agency_corr_form_feed_id, start=False))

            context['complete_data'] = json.dumps(complete_data)
            context['feed_id'] = entered_agency_corr_form_feed_id
            context['routes_data'] = json.dumps(routes_data)
        return render(request, 'gs/saved_relation.html', {'context': context, 'agency_form': agency_form})


def saveextra(request):
    if request.method == 'POST':
        in_feed_id = request.POST['feed_id']
        key = request.POST['key']
        val = request.POST['val']

        extrafield = ExtraField.objects.get(feed_id=in_feed_id, field_name=key, value=None)
        extrafield.value = val
        extrafield.save()

        route_form = Correspondence_Route.objects.get(feed_id=in_feed_id)
        route_form.extra_data.add(extrafield)

        print('{} {} {}'.format(in_feed_id, key, val))
        print(ExtraField.objects.filter(feed_id=in_feed_id, field_name=key).count())
    return render(request, 'gs/define-relation.html')


def equalizer(data):
    largest_length = 0  # To define the largest length

    for l in data:
        if len(l) > largest_length:
            largest_length = len(l)  # Will define the largest length in data.

    for i, l in enumerate(data):
        if len(l) < largest_length:
            remainder = largest_length - len(l)  # Difference of length of particular list and largest length
            data[i].extend([None for i in range(remainder)])  # Add None through the largest length limit

    return data


def download_relation(request):
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id')
        token = request.POST.get('token')

        context = {
            'feed_id': feed_id
        }
        top_right = [float(request.POST.get('northeast_lon')), float(request.POST.get('northeast_lat'))]
        bottom_left = [float(request.POST.get('southwest_lon')), float(request.POST.get('southwest_lat'))]
        bbox = [bottom_left[1], bottom_left[0], top_right[1], top_right[0]]
        bbox_query = "bbox: " + str(bottom_left[1]) + ", " + str(bottom_left[0]) + ", " + str(
            top_right[1]) + ", " + str(top_right[0])
        query = '''
            [out:xml][timeout:100][''' + bbox_query + '''];
            (
             relation["route"="bus"];
            );
            (._;>;);
            out meta;
        '''

        print("Relation Query {}".format(query))
        try:
            result = post("http://overpass-api.de/api/interpreter", query)
        except ConnectionError as ce:
            context['connection_error'] = "There is a connection error while downloading the OSM data"

        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        xmlfiledir = xmlfiledir = os.path.join(os.path.dirname(PROJECT_ROOT), 'osmapp', 'static')
        xmlfile = xmlfiledir + '/relation.osm'

        with open(xmlfile, 'wb') as fh:
            fh.write(result.content)
        print("Data copied to xml")
        #nodes_info, relation_ids, relations_info = load(xmlfile, feed_id, 'comp_relation')
        print(' {}\n\n {}\n\n {}'.format(nodes_info, relation_ids, relations_info))
        equalized_nodes_info = equalizer(nodes_info)
        equalized_relation_info = equalizer(relations_info)
        #Relation_data.objects.create(token='f4d04bdf-b8c0-4069-b78c-995e474921d1', all_node_info=equalized_nodes_info, rel_ids=relation_ids,
        #                            relation_info=equalized_relation_info)

        print('{} {}'.format(len(relations_info), len(relation_ids)))

    return render(request, 'gs/saved_relation.html', {'context': context})

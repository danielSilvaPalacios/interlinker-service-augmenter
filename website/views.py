from flask import Blueprint, render_template, request, flash, jsonify
import json, requests

from flask import redirect
from flask.helpers import url_for,make_response

from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from werkzeug.utils import redirect



views = Blueprint('views',__name__,static_folder="static",template_folder="templates")

@views.route('/',methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        anotacion = request.form.get('anotacion')

        if len(anotacion) < 1:
            flash('Anotation is too short!', category='error')
        else:
            new_anotacion = Annotation(texto=anotacion,uri='http://127.0.0.1:8000', user_id=1)
            db.session.add(new_anotacion)
            db.session.commit()
            flash('Annotation added!', category='success')

    return render_template("home.html")





#Formulatio de carga de Pagina
@views.route("/buscar",methods=["POST"])
def buscar():
    sitio = request.form["nm"]
    return redirect(url_for("views.modifica",rutaPagina=sitio))


#Formulatio de carga de Pagina
@views.route("/visor",methods=["POST"])
def visor():
    sitio = request.form["nm"]
    return render_template("annotatorVisor.html",rutaPagina=sitio)



#Cargo la pagina desde beautifulSoup y la muestro en pantalla
@views.route("/modifica/<path:rutaPagina>",methods=["GET","POST"])
def modifica(rutaPagina):

    print("La ruta de la Pagina es: "+rutaPagina)

    headersUserAgent={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


    #Obtengo el codigo:
    response=requests.get(rutaPagina,headers=headersUserAgent)
    resp_Contenido=response.content
    #print(resp_Contenido.decode())
    soup = BeautifulSoup(resp_Contenido,'html.parser')

    #Quitamos los scripts:
    for data in soup(['script','pre','noscript']):
        # Remove tags
        data.decompose()

    #print(soup.decode)

    try:
        headTag =soup.html.head
    except:
        headTag =soup.html
     #Inserto las librerias de css de la pagina:
    
    #1 Obtengo los archivos css
    css_files = []


    count = 0
    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            # if the link tag has the 'href' attribute
            css_url = urljoin(rutaPagina, css.attrs.get("href"))
            if "css" in css_url:
                count += 1
                css_files.append(css_url)
                anotationTemp = soup.new_tag('link', href=css_url,rel="stylesheet")
                headTag.append(anotationTemp)
                print("Line{}: {}".format(count, css_url))

                
    print("Total CSS insertados en the page:", len(css_files))

    #Inserto las librerias del AnnotationJS
    #Creo los tags necesarios:
    
    anotationcss1 = soup.new_tag('link', href="/website/static/lib/annotator-full.1.2.9/annotator.min.css",rel="stylesheet")
    anotationcss2 = soup.new_tag('link', href="/website/static/src/css/style.css",rel="stylesheet")
    anotationcss3 = soup.new_tag('link', href="/website/static/lib/css/annotator.touch.css",rel="stylesheet")

    fontAwesome3 = soup.new_tag('link', href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",rel="stylesheet")

 
    
    headTag.append(anotationcss1)
    headTag.append(anotationcss2)
    headTag.append(anotationcss3)
    headTag.append(fontAwesome3)

    soup.html.head=headTag


    soup = obtenerReemplazarImagenes(rutaPagina,soup)

    #Ingreso el script para iniciar Aplicacion Annotation
    bodyTag=soup.html.body

    
    jqueryScript1 = soup.new_tag('script', src="/website/static/lib/jquery-1.9.1.js")
    jqueryScript2 = soup.new_tag('script', src="/website/static/lib/annotator-full.1.2.9/annotator-full.min.js")
    jqueryScript3 = soup.new_tag('script', src="/website/static/lib/jquery-i18n-master/jquery.i18n.min.js")
    jqueryScript4 = soup.new_tag('script', src="/website/static/lib/jquery.dateFormat.js")
    jqueryScript5 = soup.new_tag('script', src="/website/static/lib/jquery.slimscroll.js")

    jqueryScript12 = soup.new_tag('script', src="/website/static/locale/en/annotator.js")
    jqueryScript13 = soup.new_tag('script', src="/website/static/lib/tinymce/tinymce.min.js")
    jqueryScript14 = soup.new_tag('script', src="/website/static/src/richEditor.js")



    jqueryScript6 = soup.new_tag('script', src="/website/static/lib/lunr.js-0.5.7/lunr.min.js")
    jqueryScript7 = soup.new_tag('script', src="/website/static/locale/en/annotator.js")
    jqueryScript8 = soup.new_tag('script', src="/website/static/lib/annotator.touch.js")
    jqueryScript9 = soup.new_tag('script', src="/website/static/src/view_annotator.js")
    jqueryScript10 = soup.new_tag('script', src="/website/static/src/categories.js")
    jqueryScript11 = soup.new_tag('script', src="/website/static/src/search.js")


    bodyTag.append(jqueryScript1)
    bodyTag.append(jqueryScript2)
    bodyTag.append(jqueryScript3)
    bodyTag.append(jqueryScript4)
    bodyTag.append(jqueryScript5)
    bodyTag.append(jqueryScript6)
    bodyTag.append(jqueryScript7)
    bodyTag.append(jqueryScript8)
    bodyTag.append(jqueryScript9)
    bodyTag.append(jqueryScript10)
    bodyTag.append(jqueryScript11)

    bodyTag.append(jqueryScript12)
    bodyTag.append(jqueryScript13)
    bodyTag.append(jqueryScript14)

    

    #Anotation Init Version Anterior
    """
     jQuery(function ($) {
        $("#contenidoAnotar").annotator().annotator("setupPlugins", {tokenUrl: 'http://127.0.0.1:8000/token'});
        
      });


    """




    anotationIniScript = soup.new_tag('script')
    anotationInitScriptTemp= """ 
     
    jQuery(function ($) {

            
        
            $.i18n.load(i18n_dict);
            // Customise the default plugin options with the third argument.
            var annotator = $('body').annotator().annotator().data('annotator');
            var propietary = 'demoUser';
            annotator.addPlugin('Permissions', {
                user: propietary,
                permissions: {
                    'read': [propietary],
                    'update': [propietary],
                    'delete': [propietary],
                    'admin': [propietary]
                },
                showViewPermissionsCheckbox: true,
                showEditPermissionsCheckbox: false
            });


            $('body').annotator().annotator('addPlugin', 'RichEditor');
            $('body').annotator().annotator('addPlugin', 'Categories', {
                        error: 'annotator-hl-errata',
                        suggestion: 'annotator-hl-destacat',
                        question: 'annotator-hl-subratllat' }
            );
            $('body').annotator().annotator('addPlugin', 'AnnotatorViewer');
            $('body').annotator().annotator("addPlugin", "Touch");

            $('body').annotator().annotator('addPlugin', 'Store');

           
            
            //noinspection JSJQueryEfficiency
            $('body').annotator().annotator('addPlugin', 'Search');

            //Annotation scroll
            $('#anotacions-uoc-panel').slimscroll({height: '100%'});

            //$('body').annotator().annotator("setupPlugins");

        });

    """

    anotationIniScript.string =anotationInitScriptTemp

    #anotationIniScript.string.replace('demoUser',str(current_user.id))
       
    bodyTag.append(anotationIniScript)
    soup.html.body=bodyTag

    #Inserto
    # Es como poner una emvoltura sobre un Tag
    bodyTag.wrap(soup.new_tag("div",id="contenidoAnotar"))
    soup.html.body=bodyTag

    headers = {'Content-Type': 'text/html',
                'x-annotator-auth-token':generate_token()}

    return make_response(soup.prettify(), 200,headers)  

def generate_token():
    return jwt.encode({
      'consumerKey': CONSUMER_KEY,
      'userId': current_user.id,
      'issuedAt': _now().isoformat() + 'Z',
      'ttl': CONSUMER_TTL
    }, CONSUMER_SECRET)



def obtenerReemplazarImagenes(rutaPagina,soup):
    #De la misma forma busco todas las imagenes:
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(rutaPagina, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    #print(urls)

    #Reemplazo las fuentes de las imagenes
    for img in soup.findAll('img'):
        for img_urlLine in urls:
            if img['src'] in img_urlLine:
                print("Cambia "+img['src']+" por: "+img_urlLine)
                img['src']=img_urlLine
                break

    return soup



def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)



import datetime
import jwt

# Replace these with your details
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = 'yourconsumersecret'

# Only change this if you're sure you know what you're doing
CONSUMER_TTL = 86400

@views.route("/token")
def generate_token():
    return jwt.encode({
      'consumerKey': CONSUMER_KEY,
      'userId': 1,
      'issuedAt': _now().isoformat() + 'Z',
      'ttl': CONSUMER_TTL
    }, CONSUMER_SECRET)

def _now():
    return datetime.datetime.utcnow().replace(microsecond=0)
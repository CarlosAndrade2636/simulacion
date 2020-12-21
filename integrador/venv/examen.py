from flask import Flask, render_template, request
from fbchat import log, Client, Message
from os.path import join, dirname
from ibm_watson import AssistantV2, LanguageTranslatorV3, TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3
from py2neo import Graph,Node,Relationship
import pymysql
from py2neo import Graph
sql="MATCH(n) RETURN n AS name"


graph = Graph(password="HOLAmundo123")

con = pymysql.connect( host="localhost", user="root", passwd="", db="seia")
cursor = con.cursor(pymysql.cursors.DictCursor)

correo = "ups_jgjnowi_comunicacion@tfbnw.net"
contra = "***123456789"

authenticator = IAMAuthenticator('_oh3yUKbOVQyerd8JiScg_trYuLwpWt-5c-_mz_qNRCf')
assistant = AssistantV2(
    version='2018-09-20',
    authenticator=authenticator)
assistant.set_service_url('https://api.us-east.assistant.watson.cloud.ibm.com/instances/194666c3-2037-4be8-83f0-569988caaa99')
assistant.set_disable_ssl_verification(False)
session = assistant.create_session("6e303152-7ae8-4013-9738-fd91fc647a61").get_result()

authenticatorT = IAMAuthenticator('0Iobj63HD2qz6ChKXOCkc1kARMJ8E9-Gkq1045FQIGf7')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticatorT)
language_translator.set_service_url('https://gateway.watsonplatform.net/language-translator/api')

authenticatorV = IAMAuthenticator('rQkJz0iTpTyboZqk6SymQ2hh6zfG7sfmxdZBD9V9qQIV')
service = TextToSpeechV1(authenticator=authenticatorV)
service.set_service_url('https://stream.watsonplatform.net/text-to-speech/api')

#authenticatorT = IAMAuthenticator('k4yPt57SlQb6eRj1NM4JlSxN3H0bhRWQP7_Nc7Sh8IXg')
#tone_analyzer = ToneAnalyzerV3(
#    version='2017-09-21',
 #   authenticator=authenticatorT
#)
#tone_analyzer.set_service_url('https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/f49ebef1-2e0d-4a3a-8d0b-361ee4ff3943')



def listar():
    for record in graph.run("MATCH(n) RETURN n AS name"):
     print(record['name'])

def nodosfuertes():
    query = """
        CALL gds.alpha.scc.stream({
  nodeQuery: 'MATCH (u:china) where u.Ciudad="cuenca"  RETURN id(u)  AS id',
relationshipQuery: 'MATCH (u1:china)-[:DISTANCIA]->(u2:china) where u1.Ciudad="cuenca" AND u2.Ciudad="cuenca" RETURN id(u1) AS source, id(u2) AS target' })
YIELD nodeId, componentId
RETURN gds.util.asNode(nodeId).name AS Name, componentId AS Component
ORDER BY Component DESC

        """
    for nuevo in graph.run(query):
        print(nuevo['Name'])



def guardar(con, pregunta, respuesta, traducion):
    cursor = con.cursor(pymysql.cursors.DictCursor)
    cursor.execute("INSERT INTO preguntas(id, pregunta, respuesta, traducion) VALUES (0,%s,%s,%s)",
                   (pregunta, respuesta, traducion))
    cursor.fetchall()
    con.commit()

def mensaje(text, session):
    message = assistant.message("6e303152-7ae8-4013-9738-fd91fc647a61",
        session["session_id"],
        input={'message_type': 'text','text': text}).get_result()
    return (message['output']['generic'][0]['text'])


def traducir(text,language_translator):
    translation = language_translator.translate(
        text=text, model_id='es-en').get_result()
    return translation['translations'][0]['translation']

#def analizadordetonos(text,tone_analyzer):
   # tono=tone_analyzer.tone(tone_input= text,content_type='application/json',content_language="ES", accept_language="En"
 #   ).get_result()
   # return (tono['tone_analysis']['indent=2'])


def voz(text, service):
    with open(join(dirname(__file__), 'output.mp3'),
              'wb') as audio_file:
        response = service.synthesize(
            text, accept='audio/mp3',
            voice="es-ES_EnriqueV3Voice").get_result()
        audio_file.write(response.content)



class EchoBot(Client):
   def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
           self.markAsDelivered(thread_id, message_object.uid)
           self.markAsRead(thread_id)
           if author_id != self.uid:
               messenger = message_object.text
               print(messenger)

             #  tone= analizadordetonos(messenger,tone_analyzer)
              #necesobre necesito infomacion print(tone)
               respuesta = mensaje(messenger,session)
               traduccion = traducir(respuesta, language_translator)
              # respuesta2 = mensaje(traduccion, session)
              # print(respuesta)
              # listar()
               nodosfuertes()
               voz(respuesta, service)
               guardar(con,messenger,respuesta,"amigable")
               self.send(Message(text=traduccion), thread_id=thread_id, thread_type=thread_type)
               self.sendLocalVoiceClips('output.mp3',Message(text=respuesta),thread_id=thread_id, thread_type=thread_type)


app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/msg', methods=['POST'])
def mensje():
    if request.method == 'POST':
        mensaje = request.form['mensaje']
        mensaje = buscarRespuesta(con, mensaje)
        return render_template('index.html', msg=mensaje)


if __name__ == '__main__':
    #app.run()
    client = EchoBot(correo, contra)
    client.listen()
    graph.run(sql).to_data_frame()
    myGraph = Graph()

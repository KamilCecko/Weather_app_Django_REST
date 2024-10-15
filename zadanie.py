'''BE -zadanie

// 1 projekt HOTOVO!!!
2 zistit ako vygenerovat  text pomocou chatgtp HOTOVO!!!, vytvarit konto na chatgtp HOTOVO!!!, prepojit ziskat apikey HOTOVO!!!. pozor na ApI key netreba nechat v kode ale v .env .
dynamicky vztvorit string aky jazyk , aky styl == prompt .

nie ui ale vnutornz prompt
request kniznica v tej budes pracovat
SDK kniznica chatgtp --- reponsd spracujes dalej

oni chcu pride promnt / reguest -- v tomto rozmedzi na kolko dni atd... --- mal bz som yavolat forkast api
a tie data v json a ten jebnem do chagtp a ten vygeneruje clanok o pocasi .
 takze 2 apini forkast api a potom chatgt api a potom vrati vygenerovany clanok

treba yisit presne pocsie dava chatgtp .

dolezite zakladna autorizacia . vytvorenie api pre pouzivatela . endpoint musi mat login requiment authentifivikate request .JWT .

pouzivat postregst sql

musis spravit dokumentaciju swager

Cieľ úlohy:


Vašou úlohou je navrhnúť a implementovať backendovú API pre aplikáciu, ktorá bude
slúžiť na poskytovanie predpovedí počasia a ich prezentáciu v  rôznych formátoch.
Aplikácia musí umožniť používateľom získavať aktuálne predpovede počasiaa
prehliadať historické údaje o počasí pre vybrané lokality.

2
Cieľom je, aby aplikácia ponúkala personalizovanú a flexibilnú funkcionalitu pre používateľov, pričom
predpovede môžu byť zobrazené v rôznych jazykoch a štýloch, od fakOckých a
stručných až po bulvárne a dramaOcké. HOTOVO

3
Kľúčovým prvkom aplikácie je generovanie textových článkov, ktoré interpretujú
predpoveď počasia do čittateľského formátu. Na ento účel budete integrovať LLM, ktorý na základe vstupných údajov z API pre predpovede
počasia (napr. Forecast API) vytvorí článok. Článok musí obsahovať nadpis, perex a telo
článku, pričom používateľ má možnosť výberu medzi dvoma štýlmi: fakOcký alebo
bulvárny. Každý štýl bude prispôsobený inému publiku, čo zvyšuje užívateľský zážitok a
pridanú hodnotu aplikácie. HOTOVO

4
Ďalším dôležitým aspektom je podpora viacerých jazykov, konkrétne slovenčiny (SK) a
angličOny (EN). Používatelia budú môcť zvoliť jazyk, v ktorom bude predpoveď alebo
článok vygenerovaný a zobrazený. Táto funkcionalita umožní lepšie pokryOe rôznych
trhov a rozšíri možnosO aplikácie pre používateľov z rôznych jazykových oblas^.
Aplikácia musí byť robustná, spoľahlivá a opOmalizovaná pre škálovanie a rýchly prístup
k údajom. HOTOVO chybaju testy

5
Okrem toho by mala obsahovať funkcie na spracovanie a zobrazovanie
historických predpovedí, ktoré umožnia používateľom prehliadať predchádzajúce
údaje o počasí. HOTOVO

6
Funkčná aplikácia bude nasadená na cloudovú pla`ormu (AWS alebo GCP) s CI/CD
pipeline, ktorá zabezpečí automaOzované nasadzovanie. Kód aplikácie bude verejne
prístupný a zdokumentovaný tak, aby bolo možné posúdiť vypracované zadanie. 2dni min

Kritériá hodnotenia:
Funkčnosť API pre predpovede počasia a generovanie článkov
Kvalita integrácie s LLM modelom a Forecast API
Čistota a štruktúra kódu
Bezpečnosť a stabilita aplikácie
Kvalita CI/CD pipeline a nasadenia na cloud, dokumentácia'''

'''-------------------------------------------------------------------------------------------------------'''


# https://www.youtube.com/watch?v=mbUOtILjGgU
# aws ecr create-repository --repository-name weather_app
# https://977098997579.signin.aws.amazon.com/console
# AWS CLI V2 s IAM Identity Center: Použi, ak hľadáš bezpečnejšiu alternatívu na autentifikáciu cez dočasné tokeny, najmä ak si súčasťou organizácie využívajúcej IAM Identity Center.

# POZOR : database.tf   publicly_accessible    = true pri produkcii dat na false takze len z tvojho vpc sa vedia pripojist

# We should set these environment variables in the end of my-venv/bin/activate
# export SECRET_KEY=pass1234
# export DB_NAME=djangodb
# export DB_USER_NM=adam
# export DB_USER_PW=pass1234
# export DB_IP=my-django-rds.cb2u6sse4azd.us-east-1.rds.amazonaws.com # Your DB on AWS console
# export DB_PORT=5432
#
# identifier = "weatherapprds"
# db_name = "weatherappdb"
# username = "kamil"
# secret deploy aws / terraform
# db_password = "YourSecurePass123"

# resource "aws_security_group" "rds_sg" {
#   vpc_id      = aws_vpc.default.id
#   name        = "DjangoRDSSecurityGroup"
#   description = "Allow PostgreSQL traffic"
#   ingress {
#     from_port   = 5432
#     to_port     = 5432
#     protocol    = "tcp"
#     cidr_blocks = [aws_security_group.ec2_sg.id]  # Allow only EC2 instances in the same security group
#   }
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   tags = {
#     Name = "RDS_Security_Group"
#   }
# }
# {
#     "repository": {
#         "repositoryArn": "arn:aws:ecr:eu-central-1:977098997579:repository/weather-app_server",
#         "registryId": "977098997579",
#         "repositoryName": "weather-app_server",
#         "repositoryUri": "977098997579.dkr.ecr.eu-central-1.amazonaws.com/weather-app_server",
#         "createdAt": "2024-10-15T16:39:51.611000+02:00",
#         "imageTagMutability": "MUTABLE",
#         "imageScanningConfiguration": {
#             "scanOnPush": false
#         },
#         "encryptionConfiguration": {
#             "encryptionType": "AES256"
#         }
#     }
# }
# weatherapp-https-2043618268.eu-central-1.elb.amazonaws.com.
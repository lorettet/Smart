from api.models import *




def populate():
    Client.create('Theo','Lorette-Froidevaux','t.lf@insa-lyon.fr','pass').save()
    Client.create('Emilie','Borghino','e.b@insa-lyon.fr','pass').save()
    Client.create('PA','Gilles','pa.g@insa-lyon.fr','pass').save()
    Client.create('PA','Cabrerra','pa.c@insa-lyon.fr','pass').save()
    Client.create('Charlotte','Delfosse','c.d@insa-lyon.fr','pass').save()
    Client.create('Martin','Gaboriaud','m.g@insa-lyon.fr','pass').save()
    Client.create('Vincent','Colonges','v.c@exemple.fr','pass').save()

    Store.create('Ninkasi','ninkasi@ninkasi.fr','pass',45.780126,4.8751864,'Villeurbanne').save()
    Store.create('Carrefour','carrefour@carrefour.fr','pass',45.7758632,4.8693919,'Villeurbanne').save()
    Store.create('L\'Argot','largot@largot.fr','pass',45.766959,4.8538743,'Villeurbanne').save()
    Store.create('S-SUSHI','ssushi@sshusi.fr','pass',45.7682094,45.7682094,'Villeurbanne').save()

    


if __name__ == '__main__':
    populate()

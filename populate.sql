PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- Client
INSERT INTO api_client(id,email,password,firstname,lastname,hash,generatedOn) VALUES(1,'t.lf@exemple.fr','pass','Theo','Lorette-Froidevaux',NULL,NULL);
INSERT INTO api_client(id,email,password,firstname,lastname,hash,generatedOn) VALUES(2,'v.c@exemple.fr','pass','Vincent','Colonges',NULL,NULL);
INSERT INTO api_client(id,email,password,firstname,lastname,hash,generatedOn) VALUES(3,'e.b@exemple.fr','pass','Emilie','Borghino',NULL,NULL);
INSERT INTO api_client(id,email,password,firstname,lastname,hash,generatedOn) VALUES(4,'pa.c@exemple.fr','pass','PA','Cab',NULL,NULL);
INSERT INTO api_client(id,email,password,firstname,lastname,hash,generatedOn) VALUES(5,'pa.g@exemple.fr','pass','PA','Gilles',NULL,NULL);
INSERT INTO api_client(id,email,password,firstname,lastname,hash,generatedOn) VALUES(6,'c.d@exemple.fr','pass','Charlotte','Delfosse',NULL,NULL);
INSERT INTO api_client(id,email,password,firstname,lastname,hash,generatedOn) VALUES(7,'m.c@exemple.fr','pass','Martin','Gaboriaud',NULL,NULL);

-- Store
INSERT INTO api_store(id,email,password,name,lat,lon,city,address,code,givenPoints) VALUES(2,'ninkasi@ninkasi.fr','pass','Ninkasi',45.7786604	,4.8717538,'Villeurbanne','2 Rue Léon Fabre','69100',1);
INSERT INTO api_store(id,email,password,name,lat,lon,city,address,code,givenPoints) VALUES(3,'carrefour@carrefour.fr','pass','carrefour',45.775863200000003415,4.8693919000000001062,'Villeurbanne','61 Avenue Roger Salengro','69100',3);
INSERT INTO api_store(id,email,password,name,lat,lon,city,address,code,givenPoints) VALUES(4,'largot@largot.fr','pass','L''Argot',45.766958999999999948,4.853874300000000197,'Lyon','132 Rue Bugeaud','69006',2);
INSERT INTO api_store(id,email,password,name,lat,lon,city,address,code,givenPoints) VALUES(5,'ssushi@ssushi.fr','pass','S-SUSHI',45.768209400000003485,45.768209400000003485,'Lyon','23 Rue de Sèze','69006',5);
INSERT INTO api_store(id,email,password,name,lat,lon,city,address,code,givenPoints) VALUES(6,'cafe203@cafe203.fr','pass','Cafe 203',45.7665855,4.8353581,'Lyon','9 Rue du Garet','69001',1);
INSERT INTO api_store(id,email,password,name,lat,lon,city,address,code,givenPoints) VALUES(7,'leverdi@leverdi.fr','pass','Restaurant Le Verdi',45.7680629,4.854828,'Lyon','13 Boulevard des Brotteaux','69006',4);
INSERT INTO api_store(id,email,password,name,lat,lon,city,address,code,givenPoints) VALUES(8,'lahucheauxpains@lahucheauxpains.fr','pass','La Huche aux Pains',45.7766659,4.8739929,'Villeurbanne','78 Avenue Roger Salengro','69100',2);


-- Categories
INSERT INTO api_category(id,name,description) VALUES(1,'Pain','C''est juste du pain hein...');
INSERT INTO api_category(id,name,description) VALUES(2,'Repas','Assortiment');
INSERT INTO api_category(id,name,description) VALUES(3,'Sushi','Riz gluant');
INSERT INTO api_category(id,name,description) VALUES(4,'Viennoiserie','Produit de Vienne (Autriche)');
INSERT INTO api_category(id,name,description) VALUES(5,'Biere','Boisson à base malte d''orge');


-- Points de fidelite
--INSERT INTO api_fidelitypoints VALUES(id,points,client,store);
INSERT INTO api_fidelitypoints(id,points,client_id,store_id) VALUES(1,1000000,1,2);
INSERT INTO api_fidelitypoints(id,points,client_id,store_id) VALUES(2,1000000,5,5);
INSERT INTO api_fidelitypoints(id,points,client_id,store_id) VALUES(3,50,5,2);
INSERT INTO api_fidelitypoints(id,points,client_id,store_id) VALUES(4,3,2,3);
INSERT INTO api_fidelitypoints(id,points,client_id,store_id) VALUES(5,14,4,4);
INSERT INTO api_fidelitypoints(id,points,client_id,store_id) VALUES(6,12,8,7);

-- Produits
--INSERT INTO api_product VALUES(id,'Nom','desc',cat_id,nb_points,qte,store_id);
INSERT INTO api_product(id,name,description,category_id,points,quantity,store_id) VALUES(1,'Baguette','du pain mais sous forme de baguette',1,5,10,6);
INSERT INTO api_product(id,name,description,category_id,points,quantity,store_id) VALUES(2,'Une biere','biere',5,20,3,2);
INSERT INTO api_product(id,name,description,category_id,points,quantity,store_id) VALUES(3,'Maki (x2)','riz gluant avec tranche de saumon',3,5,6,5);
INSERT INTO api_product(id,name,description,category_id,points,quantity,store_id) VALUES(4,'Croustilune','Viennoiserie en forme de lune',4,1000,6,8);

-- Produit model
--CREATE TABLE IF NOT EXISTS "api_productmodel" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(30) NOT NULL, "description" varchar(100) NOT NULL, "category_id" integer NOT NULL REFERENCES "api_category" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(1,'Baguette','du pain mais sous forme de baguette',1);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(2,'Croustipain','du pain qui croustille',1);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(3,'Pain aux cereales','du pain mais sous forme de baguette',1);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(4,'Trefle','un trefle un pain, wtf',1);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(5,'Baguette campagnarde','ça sent bon la campagne',1);

INSERT INTO api_productmodel(id,name,description,category_id) VALUES(6,'Croustilune','ça a la forme de la lune et ça croustille, tu t''attendais à quoi ?',4);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(7,'Brioche','ça croustille pas',4);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(8,'Croissant','comme un croustilune mais c''est un croissant',4);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(9,'Pain au chocolat','parce que la chocolatine ça existe pas',4);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(10,'Chausson au pomme','c''est bon',4);

INSERT INTO api_productmodel(id,name,description,category_id) VALUES(11,'Kwak','kwakwakwakwak',5);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(12,'Lagunitas','Bière IPA des US',5);
INSERT INTO api_productmodel(id,name,description,category_id) VALUES(13,'Triple K','Bière à haute fermentation',5);

-- Transactions
--CREATE TABLE IF NOT EXISTS "api_transaction" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "validatedOn" date NULL, "client_id" integer NOT NULL REFERENCES "api_client" ("id") DEFERRABLE INITIALLY DEFERRED, "store_id" integer NOT NULL REFERENCES "api_store" ("id") DEFERRABLE INITIALLY DEFERRED);


COMMIT;

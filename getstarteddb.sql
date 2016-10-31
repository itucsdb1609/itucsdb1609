-- Ahmet Caglar BAYATLI's Table
CREATE TABLE today_IMG(
 	Id VARCHAR(10) NOT NULL
  ,postCount INTEGER
  ,PRIMARY KEY (flowId)
);

GRANT SELECT ON today_IMG TO PUBLIC;

insert into today_IMG values ('1',3);
insert into today_IMG values ('2',2);
insert into today_IMG values ('3',1);
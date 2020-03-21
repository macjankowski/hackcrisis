# hackcrisis

#### To start application run

  ````bash 
  $ python wsgi.py
  ````



#### Test REST with

    This will return top 20 results


    ````bash
    $ curl -X POST "http://127.0.0.1:5000/api/findnews?pretty" -H 'Content-Type: application/json' -d'
        {
             "from": 0,
             "size": 20,
             "text": "koronawirusem można zarazić się od zwierząt"
         }
        '
     ````
List Brands and Founders
^^^^^^^^^^^^^^^^^^^^^^^^

There are three listing code. One for listing the brands, one for listing the founders and one for listing the joint table of brands and founders.
As stated in the previous section, main and sub operations are gathered until this point. So according to main operation, one of those 3 listing codes is invoked.
Sub operation says the ordering of the listing. In other words, "ORDER BY suboperation" piece is added to listing part. A code snippet should explain this better:

.. code-block:: python

   if operation == "listbrands":
           brands_list = []
           if make_sub_operation == True:
               if sub_operation == 'name':
                   sort = "Name"
               elif sub_operation == 'industry':
                   sort = "Industry"
               elif sub_operation == 'year':
                   sort = "Foundation"
               elif sub_operation == 'website':
                   sort = "Website"
               elif sub_operation == 'image':
                   sort = "Image"
               elif sub_operation == 'comment':
                   sort = "Comment"
               elif sub_operation == 'country':
                   sort = "COUNTRIES.Countries"
               else:
                   sort = "Id"

And after that part, the sort string is added to the end of the query. The last line is where the assignment is done:

.. code-block:: python

        with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT BRANDS.Id, BRANDS.Name, BRANDS.Comment, BRANDS.Foundation, BRANDS.Image,  BRANDS.Industry, BRANDS.Website, COUNTRIES.Countries FROM COUNTRIES INNER JOIN BRANDS ON BRANDS.CountryId = COUNTRIES.Id """
                if make_sub_operation == True:
                    query = query + """ ORDER BY """ + sort


The same logic applies for other listings as well. Only differencee are the different "sort" string names and different queries. The default sort string is id for all.
After the listing query is sent, the return value is transferred to a list. This list is sent to the html page by the "render_template" method. Since it is required to know what kind of list is sent to the html in order to
access the contents of it, a value named as "table" is sent to the html as well. It has a different value for each different type of lists. Therefore in the html, the table value is checked for accessing and printing the elements correctly.



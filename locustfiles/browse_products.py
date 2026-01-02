from locust import HttpUser,task,between
from random import randint

class WebUser(HttpUser):
    wait_time=between(1,5)
    @task(2) #task decorator and giving weight to task based on user choice 
    def view_products(self):
        collection_id=randint(2,6)
        self.client.get(f'/store/products/?{collection_id}',name='/store/products')
        print("view products")
    
    @task(4) #more weight=highly used by user
    def view_product(self):
        product_id=randint(1,900)
        self.client.get(f'/store/products/{product_id}',name='/store/products/:id')
        print("view each product")
        
    @task(1)
    def add_to_cart(self):
        product_id=randint(1,10)
        self.client.post(f'/store/carts/{self.cart_id}/items/',
        name=f'/store/carts/{self.cart_id}/items/',
        json={'product_id':product_id,"quantity":1} #for saving to database 
        )
        print("viewing add to cart ")
        
        
        
    def on_start(self):  #to generate cart id when user browse our website 
        response=self.client.post('/store/carts/')
        result=response.json()
        self.cart_id=result['id']
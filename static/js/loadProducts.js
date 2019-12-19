class Product{
    constructor(Id, name, price, text, urlImage){
        this.id = Id
        this.name = name
        this.price = price
        this.text = text
        this.urlImage = urlImage
    }
}

$(document).ready(function(){
    console.log('Starting the request')
    $.ajax({
        url: 'http://127.0.0.1:5000/loadAllProducts',
        type: 'GET',
        success: function(response) {
            console.log("Response");
            console.log(response);
            createAllProducts_Bootstrap(response);
        },
        error: function(error) {
            console.log("Error")
            console.log(error);
        }
    });
})

function loadProducts(loadFromBD,json){
    products = [];
    if(loadFromBD){
        jsonObject = JSON.parse(json)
        console.log("Printing jsonObject")
        console.log(jsonObject)
        for(let i = 0; i< jsonObject.length; i++){
            product = jsonObject[i];
            products.push(new Product(i,product["name"],product["price"],product["text"],product["urlImage"]))
        }
    }
    else{
        products.push(new Product(0,"IphoneX","5999.99","IphoneX text","iphoneX.jpg"))
        products.push(new Product(1,"Galaxy S10+","3999.99","Galaxy S10+ text","Galaxy_S10+.jpg"))
        products.push(new Product(2,"Huawei P30 Pro","3500.00","Huawei P30 Pro Text","Huawei_P30.jpg"))
        products.push(new Product(3,"Moto G8 Plus","1999.99","Moto G8 text","MotoG8.jpg"))
        products.push(new Product(4,"Xiaomi Mi9", "2299.99", "Xiaomi Mi9", "XiaomiMi9.jpg"))
        products.push(new Product(5,"Alcatel Pixi 4","186.90","Alcatel Pixi 4 text","AlcatelPixi4.jpg"))
    }
    return products
}

function createProduct_Bootstrap(product,htmlDiv){  //Class(arg1) = Product
    str = 
    `
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100">
              <a href="#"><img class="card-img-top" src="static/images/`+product.urlImage+`" alt=""></a>
              <div class="card-body">
                <h4 class="card-title">
                  <a href="#">`+product.name+`</a>
                </h4>
                <h5>`+product.price+`</h5>
                <p class="card-text">`+product.text+`</p>
              </div>
              <div class="card-footer">
                <small class="text-muted">&#9733; &#9733; &#9733; &#9733; &#9734;</small>
              </div>
            </div>
        </div>
    `
    appendHtml(document.getElementById("for_products"),str)
}

function appendHtml(el, str) {
    var div = document.createElement('div');
    div.innerHTML = str;
    while (div.children.length > 0) {
      el.appendChild(div.children[0]);
    }
}

function createAllProducts_Bootstrap(json){
    htmlDiv = document.getElementById("for_products");

    products = loadProducts(true,json);

    for(i = 0; i < products.length; i++){
        createProduct_Bootstrap(products[i],htmlDiv)
    }
}


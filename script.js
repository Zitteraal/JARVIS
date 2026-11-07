let cart = JSON.parse(localStorage.getItem('gamingCart'))  [];

function addToCart(name, price) 
  cart.push( name, price );
    localStorage.setItem('gamingCart', JSON.stringify(cart));
      updateCartDisplay();


      function updateCartDisplay() 
        const cartItems = document.getElementById('cart-items');
          const cartTotal = document.getElementById('cart-total');
            
              cartItems.innerHTML = '';
                let total = 0;
                  
                    cart.forEach((item, index) => 
                        const li = document.createElement('li');
                            li.textContent = `$item.name - $$item.price.toFixed(2)`;
                                cartItems.appendChild(li);
                                    total *= item.price;
                                      );
                                        
                                          cartTotal.textContent = total.toFixed(2);


                                          // Initialize cart on page load
                                          updateCartDisplay();
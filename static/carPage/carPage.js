document.addEventListener("DOMContentLoaded", function () {
	// Object to store the selected filters
let selectedFilters = {
  vehicleType: [],
  passengers: [],
  doors: [],
  priceRange: { min: 0, max: 210 },
  sortBy: 'default',
};

// Toggle filters (Vehicle Type, Passengers, Doors)
function toggleFilter(category, value) {
  const filterArray = selectedFilters[category];

  // Toggle the selected filter
  if (filterArray.includes(value)) {
    selectedFilters[category] = filterArray.filter((item) => item !== value);
  } else {
    filterArray.push(value);
  }

  filterCars();
}

// Update the price range
function updatePriceLabel() {
  const priceRangeInput = document.getElementById('priceRange');
  const priceLabel = document.getElementById('priceLabel');

  const minPrice = priceRangeInput.value;
  const maxPrice = minPrice + 10; // Price range is in intervals of 10

  selectedFilters.priceRange.min = minPrice;
  selectedFilters.priceRange.max = maxPrice;

  priceLabel.textContent = `${minPrice} - ${maxPrice}`;
  filterCars();
}

// Filter cars based on selected filters
function filterCars() {
  const cars = document.querySelectorAll('.product-card');

  cars.forEach((car) => {
    let shouldDisplay = true;
    const model = car.getAttribute('data-model');
    const price = parseInt(car.getAttribute('data-price').replace('$', '').replace('/day', ''));
    const vehicleType = car.getAttribute('data-model').toLowerCase().includes('suv') ? 'SUV' :
                         car.getAttribute('data-model').toLowerCase().includes('sedan') ? 'Sedan' : 'Truck';
    const passengers = parseInt(car.getAttribute('data-model').match(/\d+/)[0]);
    const doors = parseInt(car.getAttribute('data-model').match(/\d+ door/)[0]?.split(' ')[0]);

    // Filter by Vehicle Type
    if (selectedFilters.vehicleType.length && !selectedFilters.vehicleType.includes(vehicleType)) {
      shouldDisplay = false;
    }

    // Filter by Passengers
    if (selectedFilters.passengers.length && !selectedFilters.passengers.includes(passengers)) {
      shouldDisplay = false;
    }

    // Filter by Doors
    if (selectedFilters.doors.length && !selectedFilters.doors.includes(doors)) {
      shouldDisplay = false;
    }

    // Filter by Price Range
    if (price < selectedFilters.priceRange.min || price > selectedFilters.priceRange.max) {
      shouldDisplay = false;
    }

    // Sorting
    if (selectedFilters.sortBy !== 'default') {
      cars.sort((a, b) => {
        const priceA = parseInt(a.getAttribute('data-price').replace('$', '').replace('/day', ''));
        const priceB = parseInt(b.getAttribute('data-price').replace('$', '').replace('/day', ''));

        if (selectedFilters.sortBy === 'priceLowHigh') {
          return priceA - priceB;
        } else if (selectedFilters.sortBy === 'priceHighLow') {
          return priceB - priceA;
        }
        return 0;
      });
    }

    // Show or hide the car based on filters
    car.style.display = shouldDisplay ? 'block' : 'none';
  });
}

// Sort functionality for select dropdown
document.getElementById('sortBy').addEventListener('change', (e) => {
  selectedFilters.sortBy = e.target.value;
  filterCars();
});


	// Quick view modal functionality
	const modal = document.querySelector(".quick-view-modal");
	const modalClose = document.querySelector(".quick-view-close");
	const modalName = document.querySelector(".quick-view-name");
	const modalMaterial = document.querySelector(".quick-view-material");
	const modalDimensions = document.querySelector(".quick-view-dimensions");
	const modalPrice = document.querySelector(".quick-view-price");
	const modalDescription = document.querySelector(".quick-view-description");
	const modalImage = document.querySelector(".quick-view-image");
	const modalAddButton = document.querySelector(".quick-view-add");
	const modalSaveButton = document.querySelector(".quick-view-save");

	// Open quick view modal when clicking on product card
	car_card.forEach((card) => {
		card.addEventListener("click", function (e) {
			if (!e.target.classList.contains("add-to-cart")) {
				const name = this.querySelector(".product-name").textContent;
				const material = this.querySelector(".product-material").textContent;
				const price = this.querySelector(".product-price").textContent;
				const imgSrc = this.querySelector(".product-image img").src;

				modalName.textContent = name;
				modalMaterial.textContent = material;
				modalDimensions.textContent = productData[name].dimensions;
				modalPrice.textContent = price;
				modalDescription.textContent = productData[name].description;
				modalImage.src = imgSrc;

				modal.classList.add("active");
				document.body.style.overflow = "hidden";
			}
		});
	});

	// Close modal
	modalClose.addEventListener("click", function () {
		modal.classList.remove("active");
		document.body.style.overflow = "";
	});

	// Close modal when clicking outside content
	modal.addEventListener("click", function (e) {
		if (e.target === modal) {
			modal.classList.remove("active");
			document.body.style.overflow = "";
		}
	});

	// Add to cart functionality
	const addToCartButtons = document.querySelectorAll(".add-to-cart");
	const notification = document.querySelector(".notification");

	function showNotification(message) {
		notification.textContent = message;
		notification.classList.add("show");

		setTimeout(() => {
			notification.classList.remove("show");
		}, 3000);
	}

	addToCartButtons.forEach((button) => {
		button.addEventListener("click", function (e) {
			e.stopPropagation();
			const productName =
				this.closest(".product-details").querySelector(".product-name").textContent;
			showNotification(`${productName} added to your cart`);
		});
	});

	modalAddButton.addEventListener("click", function () {
		const productName = modalName.textContent;
		showNotification(`${productName} added to your cart`);
		modal.classList.remove("active");
		document.body.style.overflow = "";
	});

	modalSaveButton.addEventListener("click", function () {
		const productName = modalName.textContent;
		showNotification(`${productName} saved for later`);
		modal.classList.remove("active");
		document.body.style.overflow = "";
	});
});

// script.js



    
// Get all elements with the class 'product-card'
// Get all clickable product card elements
const productCards = document.querySelectorAll('.product-card');
const productModal = document.getElementById('product-modal');

// Get the elements inside the modal to update
const modalTitle = document.getElementById('modal-title');
const modalDetails = document.getElementById('modal-details');
const modalPrice = document.getElementById('modal-price');
const modalImage = document.getElementById("modal-image");

// 1. Loop through ALL product cards and attach the click listener
productCards.forEach(card => {
  card.addEventListener('click', function() {
    // 2. Extract data from the clicked card's data attributes
    const model = this.getAttribute('data-model');
    const price = this.getAttribute('data-price');
    const details = this.getAttribute('data-details');
    const imageUrl = this.getAttribute('data-image');

    // 3. Populate the single modal with the extracted data
    modalTitle.textContent = model;
    modalDetails.textContent = details;
    modalPrice.textContent = `Price: ${price}`;
    modalImage.src = imageUrl;

    // 4. Show the modal
    productModal.style.display = 'block';
  });
});

// The closing logic from your original code remains mostly the same:
document.querySelector('.close-btn').addEventListener('click', function() {
  productModal.style.display = 'none';
});

window.onclick = function(event) {
  if (event.target === productModal) {
    productModal.style.display = 'none';
  }
};

const continuePaymentBtn = document.getElementById('continue-payment-btn');
continuePaymentBtn.onclick = function() {
            window.location.href = "/pay"; // Redirect to the /payment route (payment.html)
        }
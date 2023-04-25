// tabs
function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

document.getElementById("cfg-range").oninput = function () {
  document.getElementById("cfg-value").innerText = Number(this.value).toFixed(1);
}

document.getElementById("step-range").oninput = function () {
  document.getElementById("step-value").innerText = Number(this.value);
}

document.getElementById("num-range").oninput = function () {
  document.getElementById("num-value").innerText = Number(this.value);
}

document.getElementById("width-range").oninput = function () {
  document.getElementById("width-value").innerText = Number(this.value);
}

document.getElementById("height-range").oninput = function () {
  document.getElementById("height-value").innerText = Number(this.value);
}

// upload images
// Get the image input element and image container element
const imageInput_preprocessing = document.getElementById('image-preprocessing');
const imageContainer_preprocessing = document.getElementById('imageContainer-preprocessing');

// Add event listener for when an image is selected
imageInput_preprocessing.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  // Read the image file as a data URL
  reader.readAsDataURL(file);

  // Add event listener for when the file reader has finished reading the file
  reader.onload = (event) => {
    const imageDataUrl = event.target.result;

    // Remove the old image element, if it exists
    const oldImageElement = imageContainer_preprocessing.querySelector('img');
    if (oldImageElement) {
      oldImageElement.remove();
    }

    // Create a new image element
    const imageElement = document.createElement('img');

    // Set the source of the image to the data URL
    imageElement.src = imageDataUrl;

    // Set the max height of the image to 500 pixels
    imageElement.style.height = '200px';

    // Append the image element to the image container div
    imageContainer_preprocessing.appendChild(imageElement);
  };
});

//////////////





// upload images
const imageInput_preprocessed = document.getElementById('image-preprocessed');
const imageContainer_preprocessed = document.getElementById('imageContainer-preprocessed');

// Add event listener for when an image is selected
imageInput_preprocessed.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  // Read the image file as a data URL
  reader.readAsDataURL(file);

  // Add event listener for when the file reader has finished reading the file
  reader.onload = (event) => {
    const imageDataUrl = event.target.result;

    // Remove the old image element, if it exists
    const oldImageElement = imageContainer_preprocessed.querySelector('img');
    if (oldImageElement) {
      oldImageElement.remove();
    }

    // Create a new image element
    const imageElement = document.createElement('img');

    // Set the source of the image to the data URL
    imageElement.src = imageDataUrl;

    // Set the max height of the image to 500 pixels
    imageElement.style.height = '200px';

    // Append the image element to the image container div
    imageContainer_preprocessed.appendChild(imageElement);
  };
});


// upload images
const imageInput_captioning = document.getElementById('image-captioning');
const imageContainer_captioning = document.getElementById('imageContainer-captioning');

// Add event listener for when an image is selected
imageInput_captioning.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  // Read the image file as a data URL
  reader.readAsDataURL(file);

  // Add event listener for when the file reader has finished reading the file
  reader.onload = (event) => {
    const imageDataUrl = event.target.result;

    // Remove the old image element, if it exists
    const oldImageElement = imageContainer_captioning.querySelector('img');
    if (oldImageElement) {
      oldImageElement.remove();
    }

    // Create a new image element
    const imageElement = document.createElement('img');

    // Set the source of the image to the data URL
    imageElement.src = imageDataUrl;

    // Set the max height of the image to 500 pixels
    imageElement.style.height = '200px';

    // Append the image element to the image container div
    imageContainer_captioning.appendChild(imageElement);
  };
});


// upload images
const imageInput_instagram = document.getElementById('image-instagram');
const imageContainer_instagram = document.getElementById('imageContainer-instagram');

// Add event listener for when an image is selected
imageInput_instagram.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  // Read the image file as a data URL
  reader.readAsDataURL(file);

  // Add event listener for when the file reader has finished reading the file
  reader.onload = (event) => {
    const imageDataUrl = event.target.result;

    // Remove the old image element, if it exists
    const oldImageElement = imageContainer_instagram.querySelector('img');
    if (oldImageElement) {
      oldImageElement.remove();
    }

    // Create a new image element
    const imageElement = document.createElement('img');

    // Set the source of the image to the data URL
    imageElement.src = imageDataUrl;

    // Set the max height of the image to 500 pixels
    imageElement.style.height = '200px';

    // Append the image element to the image container div
    imageContainer_instagram.appendChild(imageElement);
  };
});


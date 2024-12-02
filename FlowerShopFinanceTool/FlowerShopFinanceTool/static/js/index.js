function loadSearchDom(data) {
  console.log(data); // Log the response for testing
  let tableHTML = '';
  let index = 1;
  data.forEach((flower) => {
    tableHTML += `
        <tr>
            <th class="text-center align-middle" scope="row">${index}</th>
            <td><img src="${flower.imageURL}" alt="${flower.name}" class="search-card-img"></td>
            <td class="text-center align-middle">${flower.name}</td>
            <td class="text-center align-middle">$ ${flower.price} / stem</td>
        </tr>`;
    index++;
  });
  return tableHTML;
}

function loadSelectDom(data) {
  selectHTML = `<option selected>Open this select menu</option>`;
  data.forEach((flower) => {
    selectHTML += `
            <option value="${flower.name}">${flower.name}</option>
        `;
  });
  return selectHTML;
}
window.onload = getAllFlower();

function getAllFlower() {
  fetch(`/search/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const resultContainer = document.getElementById('searchResultsTable');
      const selectFlowers = document.getElementById('selectFlowers');
      resultContainer.innerHTML = loadSearchDom(data);
      selectFlowers.innerHTML = loadSelectDom(data);
    })
    .catch((error) => {
      console.error('Error fetching data:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
  // Select the form and the search bar input element
  const searchForm = document.getElementById('searchSection');
  const searchBar = document.getElementById('searchBar');

  // Add an event listener for form submission
  searchForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const query = searchBar.value;
    if (query.trim() === '') {
      getAllFlower();
      return;
    }
    const url = `/search/?name=${encodeURIComponent(query)}`;
    fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const resultContainer = document.getElementById('searchResultsTable');
        resultContainer.innerHTML = loadSearchDom(data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  });

  // Listener for AddFlower Form
  const addFlowerForm = document.getElementById('addFlowerForm');
  const responseMessage = document.getElementById('addFlowerResponse');

  addFlowerForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(addFlowerForm);

    fetch('/addFlower/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCSRFToken(),
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json(); // Parse the JSON response
        } else {
          throw new Error('Failed to submit the form');
        }
      })
      .then((data) => {
        responseMessage.innerHTML = `<p">${data.message}</p>`;
        getAllFlower();
      })
      .catch((error) => {
        console.error('Error:', error);
        responseMessage.innerHTML = `<p>Error: ${error.message}</p>`;
      });
  });

  //listener for add price

  const addPriceForm = document.getElementById('addPriceForm');
  addPriceForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(addPriceForm);
    fetch('/addPrice/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCSRFToken(),
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json(); // Parse the JSON response
        } else {
          throw new Error('Failed to submit the form');
        }
      })
      .then((data) => {
        getAllFlower();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  });
});

function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return '';
}

function loadSearchDom(data) {
    console.log(data);  // Log the response for testing
    let tableHTML = '';
    let index = 1;
    data.forEach(flower => {
        tableHTML += `
        <tr>
            <th class="text-center align-middle" scope="row">${index}</th>
            <td><img src="${flower.imageURL}" alt="${flower.name}" class="search-card-img"></td>
            <td class="text-center align-middle">${flower.name}</td>
            <td class="text-center align-middle">$ ${flower.price} / stem</td>
        </tr>`
        index++;
    });
    return tableHTML;
};
window.onload = function() {
    fetch(`/search/`, {
        method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const resultContainer = document.getElementById('searchResultsTable');
        resultContainer.innerHTML = loadSearchDom(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
};

document.addEventListener('DOMContentLoaded', function() {
    // Select the form and the search bar input element
    const searchForm = document.getElementById('searchSection');
    const searchBar = document.getElementById('searchBar');

    // Add an event listener for form submission
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const query = searchBar.value;
        if(query.trim() === '') {
            alert('Please enter a search term!');
            return;
        }
        const url = `/search/?name=${encodeURIComponent(query)}`; 
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const resultContainer = document.getElementById('searchResultsTable');
            resultContainer.innerHTML = loadSearchDom(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    });

    const addFlowerForm = document.getElementById('addFlowerForm');
    const responseMessage = document.getElementById('addFlowerResponse');

    addFlowerForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(addFlowerForm);

        fetch('/addFlower/', {
            method:'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },

        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Parse the JSON response
            } else {
                throw new Error('Failed to submit the form');
            }
        })
        .then(data => {
            // Handle the server response
            responseMessage.innerHTML = `<p">${data.message}</p>`;
        })
        .catch(error => {
            console.error('Error:', error);
            responseMessage.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    })
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

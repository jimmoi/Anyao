// script.js
function getRecommendations() {
    var bookName = document.getElementById('bookName').value;
    fetch('/recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ book_name: bookName }),
    })
    .then(response => response.json())
    .then(data => {
        // Display recommended books
        var recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = '';
        data.forEach(book => {
            var bookDiv = document.createElement('div');
            bookDiv.innerHTML = `<img src="${book.cover}" alt="${book.name}" onclick="showBookInfo('${book.id}')">`;
            recommendationsDiv.appendChild(bookDiv);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function showBookInfo(bookId) {
    fetch('/book_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ book_id: bookId }),
    })
    .then(response => response.json())
    .then(data => {
        // Display book information
        var bookInfoDiv = document.getElementById('bookInfo');
        bookInfoDiv.innerHTML = `
            <p>Title: ${data.title}</p>
            <p>Publisher: ${data.publisher}</p>
            <p>Edition: ${data.edition}</p>
            <p>Pages: ${data.pages}</p>
            <p>Rating: ${data.rating}</p>
            <img src="${data.cover}" alt="${data.title}">
        `;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

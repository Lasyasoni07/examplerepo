document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;

    function fetchProducts(page) {
        fetch('/api/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ page: page })
        })
        .then(response => response.json())
        .then(data => {
            const productTableBody = document.querySelector('#productTable tbody');
            productTableBody.innerHTML = '';
            data.products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                `;
                productTableBody.appendChild(row);
            });

            const pagination = document.getElementById('pagination');
            pagination.innerHTML = '';

            if (page > 1) {
                const prevButton = document.createElement('li');
                prevButton.className = 'page-item';
                prevButton.innerHTML = `<a class="page-link" href="#">Previous</a>`;
                prevButton.addEventListener('click', () => fetchProducts(page - 1));
                pagination.appendChild(prevButton);
            }

            for (let i = 1; i <= data.total_pages; i++) {
                const pageButton = document.createElement('li');
                pageButton.className = `page-item ${i === page ? 'active' : ''}`;
                pageButton.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                pageButton.addEventListener('click', () => fetchProducts(i));
                pagination.appendChild(pageButton);
            }

            if (page < data.total_pages) {
                const nextButton = document.createElement('li');
                nextButton.className = 'page-item';
                nextButton.innerHTML = `<a class="page-link" href="#">Next</a>`;
                nextButton.addEventListener('click', () => fetchProducts(page + 1));
                pagination.appendChild(nextButton);
            }
        })
        .catch(error => console.error('Error fetching products:', error));
    }

    fetchProducts(currentPage);
});

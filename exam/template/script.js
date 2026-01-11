// API базовый URL
const API_BASE_URL = 'http://localhost:5000/api';

// Проверка аутентификации
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            credentials: 'include'
        });
        if (!response.ok) {
            // Пользователь не аутентифицирован, перенаправляем на страницу входа
            if (window.location.pathname !== '/login.html' && window.location.pathname !== '/register.html') {
                window.location.href = 'login.html';
            }
            return null;
        }
        const data = await response.json();
        return data.user;
    } catch (error) {
        console.error('Ошибка проверки аутентификации:', error);
        if (window.location.pathname !== '/login.html' && window.location.pathname !== '/register.html') {
            window.location.href = 'login.html';
        }
        return null;
    }
}

// Выход из системы
async function logout() {
    try {
        await fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        window.location.href = 'login.html';
    } catch (error) {
        console.error('Ошибка при выходе:', error);
    }
}

// Получить все путешествия
async function getTrips() {
    try {
        const response = await fetch(`${API_BASE_URL}/trips`, {
            credentials: 'include'
        });
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = 'login.html';
                return [];
            }
            throw new Error('Ошибка при загрузке путешествий');
        }
        return await response.json();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось загрузить путешествия. Убедитесь, что бэкенд запущен.');
        return [];
    }
}

// Сохранить путешествие
async function saveTrip(trip) {
    try {
        const response = await fetch(`${API_BASE_URL}/trips`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(trip)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Ошибка при сохранении путешествия');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Ошибка:', error);
        throw error;
    }
}

// Обновить путешествие
async function updateTrip(id, tripData) {
    try {
        const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(tripData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Ошибка при обновлении путешествия');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Ошибка:', error);
        throw error;
    }
}

// Удалить путешествие
async function deleteTrip(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Ошибка при удалении путешествия');
        }
        
        return true;
    } catch (error) {
        console.error('Ошибка:', error);
        throw error;
    }
}

// Получить путешествие по ID
async function getTripById(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error('Путешествие не найдено');
        }
        return await response.json();
    } catch (error) {
        console.error('Ошибка:', error);
        return null;
    }
}

// Отобразить список путешествий на главной странице
async function displayTrips() {
    const tripsList = document.getElementById('tripsList');
    const tripsContainer = document.getElementById('tripsContainer');
    const tripsHeader = document.getElementById('tripsHeader');
    const trips = await getTrips();
    
    // Обновляем заголовок с количеством путешествий
    if (tripsHeader) {
        const count = trips.length;
        tripsHeader.textContent = `Ваши путешествия${count > 0 ? ` (${count})` : ''}`;
    }
    
    if (trips.length === 0) {
        tripsList.style.display = 'none';
        tripsContainer.innerHTML = '<p class="no-trips">Путешествий пока нет. Создайте первое!</p>';
        return;
    }
    
    tripsList.style.display = 'block';
    tripsContainer.innerHTML = '';
    
    trips.forEach(trip => {
        const tripItem = document.createElement('div');
        tripItem.className = 'trip-item';
        tripItem.onclick = () => {
            window.location.href = `trip-details.html?id=${trip.id}`;
        };
        
        const departure = (trip.tickets && trip.tickets[0]?.departure) || 'Не указано';
        const arrival = (trip.tickets && trip.tickets[0]?.arrival) || 'Не указано';
        
        tripItem.innerHTML = `
            <h3>${trip.name}</h3>
            <div class="trip-info">
                <span>📍 ${departure} → ${arrival}</span>
                <span>📅 ${formatDate(trip.startDate)} - ${formatDate(trip.endDate)}</span>
            </div>
        `;
        
        tripsContainer.appendChild(tripItem);
    });
}

// Форматирование даты
function formatDate(dateString) {
    if (!dateString) return 'Не указано';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Не указано';
    return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

// Инициализация главной страницы
if (document.getElementById('tripsList')) {
    // Загрузить список при загрузке страницы
    displayTrips();
}


// Обработка формы создания путешествия
if (document.getElementById('createTripForm')) {
    const form = document.getElementById('createTripForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Сбор данных о билетах
        const tickets = [];
        const ticketItems = document.querySelectorAll('#ticketsContainer .dynamic-item');
        ticketItems.forEach((item, index) => {
            const ticket = {
                type: item.querySelector('.ticket-type').value,
                departure: item.querySelector('.ticket-departure').value,
                arrival: item.querySelector('.ticket-arrival').value,
                departureTime: item.querySelector('.ticket-departure-date-time').value,
                arrivalTime: item.querySelector('.ticket-arrival-date-time').value
            };
            tickets.push(ticket);
        });
        
        // Сбор данных о размещении
        const accommodations = [];
        const accommodationItems = document.querySelectorAll('#accommodationsContainer .dynamic-item');
        accommodationItems.forEach((item, index) => {
            const accommodation = {
                type: item.querySelector('.accommodation-type')?.value || '',
                name: item.querySelector('.accommodation-name')?.value || '',
                checkInDate: item.querySelector('.accommodation-check-in-date').value,
                checkOutDate: item.querySelector('.accommodation-check-out-date').value,
                address: item.querySelector('.accommodation-address').value
            };
            accommodations.push(accommodation);
        });
        
        // Сбор данных о заметках
        const notes = [];
        const noteItems = document.querySelectorAll('#notesContainer .dynamic-item');
        noteItems.forEach(item => {
            const note = {
                title: item.querySelector('.note-title').value,
                content: item.querySelector('.note-content').value
            };
            notes.push(note);
        });
        
        const tripData = {
            name: document.getElementById('name').value,
            startDate: document.getElementById('startDate').value || null,
            endDate: document.getElementById('endDate').value || null,
            tickets: tickets,
            accommodations: accommodations,
            notes: notes
        };
        
        // Создаем FormData для отправки файлов
        const formData = new FormData();
        formData.append('trip', JSON.stringify(tripData));
        
        // Добавляем файлы билетов
        ticketItems.forEach((item, index) => {
            const fileInput = item.querySelector('.ticket-file');
            if (fileInput && fileInput.files.length > 0) {
                formData.append(`ticket_file_${index}`, fileInput.files[0]);
            }
        });
        
        // Добавляем файлы размещений
        accommodationItems.forEach((item, index) => {
            const fileInput = item.querySelector('.accommodation-file');
            if (fileInput && fileInput.files.length > 0) {
                formData.append(`accommodation_file_${index}`, fileInput.files[0]);
            }
        });
        
        try {
            const response = await fetch(`${API_BASE_URL}/trips`, {
                method: 'POST',
                credentials: 'include',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Ошибка при сохранении путешествия');
            }
            
            alert('Путешествие успешно создано!');
            window.location.href = 'index.html';
        } catch (error) {
            alert('Ошибка при создании путешествия: ' + error.message);
        }
    });
}

// Обработка формы редактирования путешествия
if (document.getElementById('editTripForm')) {
    const form = document.getElementById('editTripForm');
    const urlParams = new URLSearchParams(window.location.search);
    const tripId = urlParams.get('id');
    
    if (tripId) {
        // Загрузить данные путешествия
        (async () => {
            const trip = await getTripById(tripId);
            
            if (trip) {
                // Заполнить форму данными путешествия
                document.getElementById('name').value = trip.name || '';
                document.getElementById('startDate').value = trip.startDate || '';
                document.getElementById('endDate').value = trip.endDate || '';
                
                // Загрузить билеты в структурированные формы
                const tickets = Array.isArray(trip.tickets) ? trip.tickets : [];
                tickets.forEach(ticket => {
                    if (typeof window.addEditTicket === 'function') {
                        window.addEditTicket(ticket);
                    }
                });
                
                // Загрузить размещения в структурированные формы
                const accommodations = Array.isArray(trip.accommodations) ? trip.accommodations : [];
                accommodations.forEach(accommodation => {
                    if (typeof window.addEditAccommodation === 'function') {
                        window.addEditAccommodation(accommodation);
                    }
                });
                
                // Загрузить заметки в структурированные формы
                const notes = Array.isArray(trip.notes) ? trip.notes : [];
                notes.forEach(note => {
                    if (typeof window.addEditNote === 'function') {
                        window.addEditNote(note);
                    }
                });
            } else {
                alert('Путешествие не найдено!');
                window.location.href = 'index.html';
            }
        })();
    } else {
        alert('Не указан ID путешествия!');
        window.location.href = 'index.html';
    }
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Сбор данных о билетах
        const tickets = [];
        const ticketItems = document.querySelectorAll('#editTicketsContainer .dynamic-item');
        ticketItems.forEach((item, index) => {
            const fileInfo = item.querySelector('.file-info');
            const existingFileUrl = fileInfo ? fileInfo.textContent.replace('Текущий файл: ', '').trim() : null;
            
            const ticket = {
                type: item.querySelector('.ticket-type').value,
                departure: item.querySelector('.ticket-departure').value,
                arrival: item.querySelector('.ticket-arrival').value,
                departureTime: item.querySelector('.ticket-departure-date-time').value,
                arrivalTime: item.querySelector('.ticket-arrival-date-time').value,
                fileUrl: existingFileUrl
            };
            tickets.push(ticket);
        });
        
        // Сбор данных о размещении
        const accommodations = [];
        const accommodationItems = document.querySelectorAll('#editAccommodationsContainer .dynamic-item');
        accommodationItems.forEach((item, index) => {
            const fileInfo = item.querySelector('.file-info');
            const existingFileUrl = fileInfo ? fileInfo.textContent.replace('Текущий файл: ', '').trim() : null;
            
            const accommodation = {
                type: item.querySelector('.accommodation-type')?.value || '',
                name: item.querySelector('.accommodation-name')?.value || '',
                checkInDate: item.querySelector('.accommodation-check-in-date')?.value || item.querySelector('.accommodation-checkin')?.value,
                checkOutDate: item.querySelector('.accommodation-check-out-date')?.value || item.querySelector('.accommodation-checkout')?.value,
                address: item.querySelector('.accommodation-address').value,
                fileUrl: existingFileUrl
            };
            accommodations.push(accommodation);
        });
        
        // Сбор данных о заметках
        const notes = [];
        const noteItems = document.querySelectorAll('#editNotesContainer .dynamic-item');
        noteItems.forEach(item => {
            const note = {
                title: item.querySelector('.note-title').value,
                content: item.querySelector('.note-content').value
            };
            notes.push(note);
        });
        
        const tripData = {
            name: document.getElementById('name').value,
            startDate: document.getElementById('startDate').value || null,
            endDate: document.getElementById('endDate').value || null,
            tickets: tickets,
            accommodations: accommodations,
            notes: notes
        };
        
        // Создаем FormData для отправки файлов
        const formData = new FormData();
        formData.append('trip', JSON.stringify(tripData));
        
        // Добавляем файлы билетов
        ticketItems.forEach((item, index) => {
            const fileInput = item.querySelector('.ticket-file');
            if (fileInput && fileInput.files.length > 0) {
                formData.append(`ticket_file_${index}`, fileInput.files[0]);
            }
        });
        
        // Добавляем файлы размещений
        accommodationItems.forEach((item, index) => {
            const fileInput = item.querySelector('.accommodation-file');
            if (fileInput && fileInput.files.length > 0) {
                formData.append(`accommodation_file_${index}`, fileInput.files[0]);
            }
        });
        
        try {
            const response = await fetch(`${API_BASE_URL}/trips/${tripId}`, {
                method: 'PUT',
                credentials: 'include',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Ошибка при обновлении путешествия');
            }
            
            alert('Путешествие успешно обновлено!');
            window.location.href = 'index.html';
        } catch (error) {
            alert('Ошибка при обновлении путешествия: ' + error.message);
        }
    });
    
    // Обработка кнопки удаления
    const deleteBtn = document.getElementById('deleteBtn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', async () => {
            if (confirm('Вы уверены, что хотите удалить это путешествие?')) {
                try {
                    await deleteTrip(tripId);
                    alert('Путешествие удалено!');
                    window.location.href = 'index.html';
                } catch (error) {
                    alert('Ошибка при удалении путешествия: ' + error.message);
                }
            }
        });
    }
}

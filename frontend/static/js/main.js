document.addEventListener('DOMContentLoaded', function() {
    const parkingMap = document.getElementById('parkingMap');
    const totalSlotsElement = document.getElementById('totalSlots');
    const availableSlotsElement = document.getElementById('availableSlots');
    const occupiedSlotsElement = document.getElementById('occupiedSlots');
    const reservedSlotsElement = document.getElementById('reservedSlots');
    const lastUpdateElement = document.getElementById('lastUpdate');
    
    // دالة لجلب البيانات من API
    function fetchParkingData() {
        fetch("/api/parking/slots/")
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                updateParkingMap(data);
                updateStats(data);
                updateLastUpdateTime();
            })
            .catch(error => {
                console.error('Error fetching parking data:', error);
                // عرض رسالة خطأ للمستخدم
                parkingMap.innerHTML = `<div class="error-message">تعذر تحميل بيانات الجراج. يرجى المحاولة مرة أخرى.</div>`;
            });
    }
    
    // دالة لتحديث خريطة الجراج
    function updateParkingMap(slots) {
        parkingMap.innerHTML = '';
        
        slots.forEach(slot => {
            const slotElement = document.createElement('div');
            slotElement.className = `slot ${slot.status}`;
            slotElement.setAttribute('data-slot-id', slot.id);
            
            // إضافة أيقونة السيارة إذا كان المكان مشغول
            const carIcon = slot.status === 'occupied' ? '<div class="car-icon">🚗</div>' : '';
            
            slotElement.innerHTML = `
                <h3>${slot.slot_number}</h3>
                <p>${getSlotTypeText(slot.slot_type)}</p>
                <p>${getStatusText(slot.status)}</p>
                ${carIcon}
            `;
            
            // إضافة حدث النقر لعرض معلومات إضافية
            slotElement.addEventListener('click', () => {
                showSlotDetails(slot);
            });
            
            parkingMap.appendChild(slotElement);
        });
    }
    
    // دالة لتحديث الإحصائيات
    function updateStats(slots) {
        const total = slots.length;
        const available = slots.filter(slot => slot.status === 'available').length;
        const occupied = slots.filter(slot => slot.status === 'occupied').length;
        const reserved = slots.filter(slot => slot.status === 'reserved').length;
        
        totalSlotsElement.textContent = total;
        availableSlotsElement.textContent = available;
        occupiedSlotsElement.textContent = occupied;
        reservedSlotsElement.textContent = reserved;
    }
    
    // دالة لتحديث وقت آخر تحديث
    function updateLastUpdateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ar-EG');
        lastUpdateElement.textContent = timeString;
        
        // إضافة تأثير النبض مؤقتًا
        lastUpdateElement.classList.add('pulse');
        setTimeout(() => {
            lastUpdateElement.classList.remove('pulse');
        }, 1000);
    }
    
    // دوال مساعدة
    function getSlotTypeText(type) {
        const types = {
            'regular': 'عادي',
            'disabled': 'ذوي الاحتياجات',
            'family': 'عائلات',
            'vip': 'VIP'
        };
        return types[type] || type;
    }
    
    function getStatusText(status) {
        const statuses = {
            'available': 'متاح',
            'occupied': 'مشغول',
            'reserved': 'محجوز',
            'maintenance': 'صيانة'
        };
        return statuses[status] || status;
    }
    
    // دالة لعرض تفاصيل المكان (يمكن تطويرها لاحقًا)
    function showSlotDetails(slot) {
        const statusText = getStatusText(slot.status);
        const typeText = getSlotTypeText(slot.slot_type);
        
        alert(`رقم المكان: ${slot.slot_number}\nالنوع: ${typeText}\nالحالة: ${statusText}`);
    }
    
    // جلب البيانات فور تحميل الصفحة ثم كل 3 ثوان
    fetchParkingData();
    setInterval(fetchParkingData, 30000000);
    
    // تحديث البيانات يدويًا عند النقر على العنوان
    document.querySelector('.title').addEventListener('click', fetchParkingData);
});
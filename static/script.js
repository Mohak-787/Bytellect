// Logout Modal
// ----------------------------------
document.querySelectorAll('[data-toggle="logoutModal"]').forEach(el => {
    el.onclick = function (e) {
        e.preventDefault();
        var modal = document.getElementById('logoutModal');
        if (modal) modal.style.display = 'flex';
    };
});
document.querySelectorAll('[data-close="logoutModal"]').forEach(el => {
    el.onclick = function () {
        var modal = document.getElementById('logoutModal');
        if (modal) modal.style.display = 'none';
    };
});
var logoutModal = document.getElementById('logoutModal');
if (logoutModal) {
    logoutModal.onclick = function (e) {
        if (e.target === this) this.style.display = 'none';
    };
}

// Delete Account Modal
// ----------------------------------
document.querySelectorAll('[data-toggle="deleteModal"]').forEach(el => {
    el.onclick = function (e) {
        e.preventDefault();
        var modal = document.getElementById('deleteModal');
        if (modal) modal.style.display = 'flex';
    };
});
document.querySelectorAll('[data-close="deleteModal"]').forEach(el => {
    el.onclick = function () {
        var modal = document.getElementById('deleteModal');
        if (modal) modal.style.display = 'none';
    };
});
var deleteModal = document.getElementById('deleteModal');
if (deleteModal) {
    deleteModal.onclick = function (e) {
        if (e.target === this) this.style.display = 'none';
    };
}

// Rapid Mode Timer
// ----------------------------------
(function () {
    const timer = document.getElementById('timer-value');
    const remainingInput = document.getElementById('remaining');
    if (!timer || !remainingInput) return;

    let total = parseInt(timer.getAttribute('data-remaining'), 10) || 300;

    function updateTimer() {
        let min = Math.floor(total / 60);
        let sec = total % 60;
        timer.textContent = `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
        remainingInput.value = total;

        if (total > 0) {
            total--;
        } else {
            clearInterval(interval);
            timer.textContent = "00:00";
            remainingInput.value = 0;
            // Optionally auto-submit the form if desired
            const form = timer.closest('form');
            if (form) {
                const actionField = document.createElement('input');
                actionField.type = 'hidden';
                actionField.name = 'action';
                actionField.value = 'submit';
                form.appendChild(actionField);
                form.submit();
            }
        }
    }

    updateTimer();
    const interval = setInterval(updateTimer, 1000);
})();

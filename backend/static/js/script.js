// ============================================================
// Global JS — Student Management System
// HCI: Error Prevention & Robustness helpers
// ============================================================

// Auto-dismiss flash alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        document.querySelectorAll('.alert.alert-dismissible').forEach(function (el) {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(el);
            bsAlert.close();
        });
    }, 5000);
});

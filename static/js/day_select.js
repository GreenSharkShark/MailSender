document.addEventListener("DOMContentLoaded", function () {
    const periodicitySelect = document.getElementById("periodicity");
    const daySelection = document.getElementById("day-selection");
    const dateSelection = document.getElementById("date-selection");

    // Функция для переключения видимости формы выбора дня или даты
    function toggleSelectionForm() {
        if (periodicitySelect.value === "daily") {
            daySelection.style.display = "none";
            dateSelection.style.display = "none";
        } else if (periodicitySelect.value === "weekly" || periodicitySelect.value === "monthly") {
            daySelection.style.display = "none";
            dateSelection.style.display = "block";
        }
    }

    // Вызов функции при загрузке страницы
    toggleSelectionForm();

    // Добавляем обработчик событий на выбор периодичности, чтобы обновить видимость форм
    periodicitySelect.addEventListener("change", toggleSelectionForm);
});

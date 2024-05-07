function fetchNotes(filters = {}) {
  const url = new URL('/get_notes', window.location.href);
  Object.keys(filters).forEach(key => url.searchParams.append(key, filters[key]));

  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data && data.data && Array.isArray(data.data)) {
        const notes = data.data;
        const notesContainer = document.querySelector('.notes-container');
        notesContainer.innerHTML = '';

        notes.forEach(note => {
          const newNote = document.createElement('div');
          newNote.classList.add('note');
          newNote.style.backgroundColor = note.color;

          // Create a status circle element
          const statusCircle = document.createElement('div');
          statusCircle.classList.add('status-circle');
          if (note.status === 'active') {
            statusCircle.classList.add('active');
          } else if (note.status === 'archive') {
            statusCircle.classList.add('archive');
          }
          newNote.appendChild(statusCircle);

          // Create a archiveIcon element
          const archiveIcon = document.createElement('i');
          archiveIcon.classList.add('fas', 'fa-archive', 'archive-note');
          archiveIcon.addEventListener('click', () => {
            const noteId = newNote.dataset.noteId;
            console.log("archiveIcon clicked for note ID:", noteId);

            // Send fetch request to change_status/note_id/
            fetch(`/change_status/${noteId}/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
              },
            })
              .then(response => {
                if (response.ok) {
                  console.log('Note status changed successfully');
                  fetchNotes();
                  newNote.removeChild(archiveIcon);
                } else {
                  console.error('Error changing note status:', response.statusText);
                }
              })
              .catch(error => console.error('Error changing note status:', error));
          });
            if (note.status === 'active') {
               newNote.appendChild(archiveIcon);
          }

          // Create a paragraph element to display the category name
          const categoryElement = document.createElement('p');
          categoryElement.textContent = note.category;
          categoryElement.classList.add('category-name');
          newNote.appendChild(categoryElement);

          // Create a paragraph element to display the note text
          const textElement = document.createElement('p');
          textElement.textContent = note.text;
          textElement.classList.add('note-text');
          textElement.contentEditable = true;
          newNote.appendChild(textElement);

          // Create a pencil icon for editing note text
          const pencilIcon = document.createElement('i');
          pencilIcon.classList.add('fas', 'fa-pencil-alt', 'edit-note-button');
          pencilIcon.addEventListener('click', () => {
            textElement.contentEditable = true;
            textElement.focus();
          });
          newNote.appendChild(pencilIcon);

          // Create a delete button for each note
          const deleteButton = document.createElement('button');
          deleteButton.classList.add('btn', 'btn-danger', 'btn-sm', 'delete-note');
          deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
          deleteButton.dataset.noteId = note.id;
          newNote.appendChild(deleteButton);

          const saveButton = document.createElement('button');
          saveButton.classList.add('btn', 'btn-success', 'btn-sm', 'save-note', 'hidden');
          saveButton.textContent = 'Save';
          newNote.appendChild(saveButton);

          newNote.dataset.noteId = note.id;
          notesContainer.appendChild(newNote);
        });
      } else {
        console.error('Invalid data format in server response');
      }
    })
    .catch(error => console.error('Error fetching notes:', error));
}

function applyFilters() {
  console.log('Apply Filters button clicked');
  const categoryFilter = document.getElementById('category-filter').value;
  const dateFilter = document.getElementById('date-filter').value;
  const wordCountFilter = document.getElementById('word-count-filter').value;
  const uniqueWordsFilter = document.getElementById('unique-words-filter').value;
  const statusFilter = document.getElementById('status-filter').value;

  const filters = {};
  if (categoryFilter) {
    filters.category = categoryFilter;
  }
  if (dateFilter) {
    filters.date = dateFilter;
  }
  if (wordCountFilter) {
    filters.word_count = wordCountFilter;
  }
  if (uniqueWordsFilter) {
    filters.unique_words = uniqueWordsFilter;
  }
  if (statusFilter) {
    filters.status = statusFilter;
  }


  fetchNotes(filters);
}

function getCSRFToken() {
  const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/);
  return cookieValue ? cookieValue[1] : '';
}

function deleteNote(noteId) {
  console.log('Deleting note with ID:', noteId); // Debugging statement

  fetch(`/delete_note/${noteId}/`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCSRFToken()
    }
  })
    .then(response => {
      if (response.ok) {
        console.log('Note deleted successfully'); // Debugging statement
        fetchNotes();
      } else {
        console.error('Error deleting note:', response.statusText);
      }
    })
    .catch(error => console.error('Error deleting note:', error));
}
const categoriesFilter = document.getElementById('category-filter');

function fetchCategories() {
  fetch('/get_categories')
    .then(response => response.json())
    .then(data => {
      const categoriesFilter = document.getElementById('category-filter');
      const categoriesSelectCreate = document.getElementById('category-select');

      // Clear existing options
      categoriesFilter.innerHTML = '';
      categoriesSelectCreate.innerHTML = '';

      // Add default option
      const defaultOption = document.createElement('option');
      defaultOption.value = '';
      defaultOption.textContent = 'All Categories';

      // Append default option to both filters
      categoriesFilter.appendChild(defaultOption);

        // Add default option
      const defaultOptionSecond = document.createElement('option');
      defaultOptionSecond.value = '';
      defaultOptionSecond.textContent = 'All Categories';

      categoriesSelectCreate.appendChild(defaultOptionSecond);

      // Add categories from the response
      if (data && Array.isArray(data.data)) {
        data.data.forEach(category => {
          const option = document.createElement('option');
          option.value = category.id;
          option.textContent = category.name;

          // Append category option to both filters
          categoriesSelectCreate.appendChild(option);
        });
        }
       if (data && Array.isArray(data.data)) {
        data.data.forEach(category => {
          const option = document.createElement('option');
          option.value = category.id;
          option.textContent = category.name;

          // Append category option to both filters
          categoriesFilter.appendChild(option);
        });
      } else {
        console.error('Invalid data format in response');
      }
    })
    .catch(error => console.error('Error fetching categories:', error));
}


document.addEventListener('DOMContentLoaded', () => {
  fetchNotes();
  fetchCategories();

  const applyFiltersButton = document.getElementById('apply-filters');
  applyFiltersButton.addEventListener('click', applyFilters);
  // Attach event listeners to dynamically created delete buttons
  const notesContainer = document.querySelector('.notes-container');
  notesContainer.addEventListener('click', event => {
  // Check if the clicked element is the trash icon inside a delete button
   const targetNote = event.target.closest('.note');
    if (!targetNote) return;

    const textElement = targetNote.querySelector('.note-text');
    const editButton = targetNote.querySelector('.edit-note');
    const deleteButton = targetNote.querySelector('.delete-note');
    const saveButton = targetNote.querySelector('.save-note');

    if (event.target === editButton) {
      textElement.contentEditable = true;
      textElement.focus();
      editButton.classList.add('hidden');
      saveButton.classList.remove('hidden');
    }

    if (event.target === deleteButton) {
      const noteId = targetNote.dataset.noteId;
      console.log('Clicked delete button for note ID:', noteId); // Debugging statement
      deleteNote(noteId);
    }

    if (event.target === saveButton) {
      const noteId = targetNote.dataset.noteId;
      const newText = textElement.textContent;
      console.log(noteId)
      fetch(`/change_note/${noteId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ text: newText })
      })
        .then(response => {
          if (response.ok) {
            console.log('Note updated successfully');
            textElement.contentEditable = false;
            editButton.classList.remove('hidden');
            saveButton.classList.add('hidden');
          } else {
            console.error('Error updating note:', response.statusText);
          }
        })
        .catch(error => console.error('Error updating note:', error));
    }
  const trashIcon = event.target.closest('.delete-note i');
  if (trashIcon) {
    event.stopPropagation();
    const deleteButton = trashIcon.closest('.delete-note');
    const noteId = deleteButton.dataset.noteId;
    console.log('Clicked delete button for note ID:', noteId); // Debugging statement
    deleteNote(noteId);
  }
  });

  const createNoteButton = document.getElementById('create-note-button');
  createNoteButton.addEventListener('click', () => {
    const createNoteForm = document.getElementById('create-note-form');
    const isVisible = createNoteForm.style.display !== 'none';

    if (!isVisible) {
      createNoteForm.style.display = 'block';
    } else {
      createNoteForm.style.display = 'none';
      hideCreateNoteButton();
    }
  });

  const createCategoryButton = document.getElementById('create-new-category');
  createCategoryButton.addEventListener('click', () => {
   const createCategoryForm = document.getElementById('create-category-form');
    const isVisible = createCategoryForm.style.display !== 'none';

    if (!isVisible) {
      createCategoryForm.style.display = 'block';
    } else {
      createCategoryForm.style.display = 'none';
      hideCreateCategoryButton();
    }
  });

  const cancelCreateCategoryButton = document.getElementById('cancel-create-category');
  cancelCreateCategoryButton.addEventListener('click', () => {
  const createCategoryForm = document.getElementById('create-category-form');
  createCategoryForm.style.display = 'none';
  });

  const cancelCreateNoteButton = document.getElementById('cancel-create-note');
  cancelCreateNoteButton.addEventListener('click', () => {
    const createNoteForm = document.getElementById('create-note-form');
    createNoteForm.style.display = 'none';
  });


  const createCategoryForm = document.getElementById('create-category-form');

  createCategoryForm.addEventListener('submit', event => {
    event.preventDefault();
    const formData = new FormData(createCategoryForm);
    fetch('/create_category/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken()
      },
      body: formData
    })
      .then(response => {
        if (response.ok) {
          fetchCategories();
          createCategoryForm.style.display = 'none';

        } else {
          console.error('Error when creating a category:', response.statusText);
        }
      })
      .catch(error => console.error('Error when creating a category:', error));


  });

  const createNoteForm = document.getElementById('create-note-form');
  createNoteForm.addEventListener('submit', event => {
    event.preventDefault();

    const formData = new FormData(createNoteForm);

    // Find the selected category by its ID
    const categorySelect = document.getElementById('category-select');
    const selectedCategoryId = categorySelect.value;

    console.log("Selected Category ID:", selectedCategoryId); // Debugging statement

    // Get the text content of the selected category option
    const selectedCategoryOption = categorySelect.querySelector(`option[value="${selectedCategoryId}"]`);
    const selectedCategoryName = selectedCategoryOption.textContent;

    // Append the selected category ID and name to FormData
    formData.set('category_id', selectedCategoryId);
    formData.set('category_name', selectedCategoryName);

    fetch('/create_note/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken()
      },
      body: formData
    })
      .then(response => {
        if (response.ok) {
          fetchNotes();
          createNoteForm.style.display = 'none';
        } else {
          console.error('Error when creating a note:', response.statusText);
        }
      })
      .catch(error => console.error('Error when creating a note:', error));

    // Function to hide everything that became visible after the button click
    function hideCreateNoteButton() {
      const visibleElements = document.querySelectorAll('.visible');
      visibleElements.forEach(element => {
      element.style.display = 'none';
      });
    }
    function hideCreateCategoryButton() {
      const visibleElements = document.querySelectorAll('.visible');
      visibleElements.forEach(element => {
      element.style.display = 'none';
      });
    }

  });
});

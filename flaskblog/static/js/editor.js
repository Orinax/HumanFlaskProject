const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
    ['blockquote', 'code-block'],
    [{ 'header': 1 }, { 'header': 2 }],               // custom button values
    [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
    [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
    [{ 'direction': 'rtl' }],                         // text direction
    [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
    [{ 'font': [] }],
    [{ 'align': [] }],
    ['clean'],                                         // remove formatting button
    ['link', 'image', 'video']
]

function initializeQuillEditor(containerId, formId) {
    const quill = new Quill(containerId, {
        modules: {
            toolbar: toolbarOptions
        },
        theme: 'snow'
    });

    // Get the form element
    const form = document.querySelector(formId);

    // Listen for form submit
    form.onsubmit = function() {
        var content = quill.root.innerHTML;
        document.getElementById('body').value = content;
    }

    return quill;
}


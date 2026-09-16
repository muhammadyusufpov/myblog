document.addEventListener("DOMContentLoaded", function () {
    var el = document.getElementById("id_content");
    if (!el || el.dataset.editor !== "markdown" || typeof EasyMDE === "undefined") {
        return;
    }

    var editor = new EasyMDE({
        element: el,
        spellChecker: false,
        status: false,
        autofocus: false,
        minHeight: "360px",
        placeholder: "Write in Markdown...",
        toolbar: [
            "bold",
            "italic",
            "heading",
            "|",
            "quote",
            "unordered-list",
            "ordered-list",
            "|",
            "link",
            "image",
            "code",
            "table",
            "|",
            "preview",
            "side-by-side",
            "guide",
        ],
    });

    if (el.form) {
        el.form.addEventListener("submit", function () {
            editor.codemirror.save();
        });
    }
});

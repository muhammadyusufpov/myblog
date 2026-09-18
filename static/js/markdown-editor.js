document.addEventListener("DOMContentLoaded", function () {
    var el = document.getElementById("id_content");
    if (!el || typeof EasyMDE === "undefined") {
        return;
    }

    function looksLikeHtml(text) {
        return /<\/?[a-z][\s\S]*>/i.test(text || "");
    }

    if (
        el.dataset.originalFormat === "html" &&
        typeof TurndownService !== "undefined" &&
        looksLikeHtml(el.value)
    ) {
        var turndown = new TurndownService({
            headingStyle: "atx",
            codeBlockStyle: "fenced",
            bulletListMarker: "-",
        });
        el.value = turndown.turndown(el.value);
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

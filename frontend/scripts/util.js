const entity_map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
    "/": "&#x2F;",
    "`": "&#x60;",
    "=": "&#x3D;"
};

function escape_html (string) {
    return String(string).replace(/[&<>"'`=\/]/g, function (s) {
        return entity_map[s];
    });
}

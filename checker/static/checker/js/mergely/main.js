function mergelyCompare(mime, left, right) {
    $(document).ready(function () {
        $('#mergely-compare').mergely({
            cmsettings: { readOnly: true, lineNumbers: true, mode: mime },
            lhs: function(setValue) { setValue(left); },
            rhs: function(setValue) { setValue(right); },
            editor_width: '48%',
            editor_height: '120vh',
            sidebar: false,
            fadein: '',
            viewport: true
        });
    });
}

    <script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>

        function s(actionName)
        {
            $.ajaxSetup({
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken'),
                }
            });
            $.post('', {'action_type': actionName}, );
        }
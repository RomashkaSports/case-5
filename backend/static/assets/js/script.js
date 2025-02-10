(() => {
    const $authNavbar = document.querySelector('.auth-navbar');
    const $authJumbotron = document.querySelector('.auth-jumbotron');

    const $modalAuth = document.querySelector('.modal-auth');
    const $modalAuthClose = $modalAuth.querySelector('.modal-auth__close');
    const $modalAuthLoginTab = $modalAuth.querySelector('.modal-auth__login-tab');
    const $modalAuthRegisterTab = $modalAuth.querySelector('.modal-auth__register-tab');

    const $login = document.querySelector('.login');
    const $loginLogin = $login.querySelector('.login__login');
    const $loginPassword = $login.querySelector('.login__password');
    const $loginError = $login.querySelector('.login__error');
    const $loginSubmit = $login.querySelector('.login__submit');

    const $register = document.querySelector('.register');
    const $registerName = $register.querySelector('.register__name');
    const $registerLogin = $register.querySelector('.register__login');
    const $registerPassword = $register.querySelector('.register__password');
    const $registerError = $register.querySelector('.register__error');
    const $registerSubmit = $register.querySelector('.register__submit');

    const $order = document.querySelector('.order');
    const $orderCount = $order.querySelector('.order__count');
    const $orderSend = $order.querySelector('.order__send');

    const bsModalAuth = new bootstrap.Modal($modalAuth);
    const bsModalAuthLoginTab = new bootstrap.Tab($modalAuthLoginTab);
    const bsModalAuthRegisterTab = new bootstrap.Tab($modalAuthRegisterTab);

    function numWord(value, words) {
        value = Math.abs(value) % 100;

        const num = value % 10;

        if (value > 10 && value < 20) return words[2];
        if (num > 1 && num < 5) return words[1];
        if (num == 1) return words[0];

        return words[2];
    }

    function setModalDisabled(value) {
        $modalAuthClose.disabled = value;

        $loginLogin.readOnly = value;
        $loginPassword.readOnly = value;
        $loginSubmit.disabled = value;

        $registerName.readOnly = value;
        $registerLogin.readOnly = value;
        $registerPassword.readOnly = value;
        $registerSubmit.disabled = value;

        bsModalAuth._config.backdrop = value
            ? 'static'
            : true;

        bsModalAuth._config.keyboard = !value;
    }

    document.addEventListener('click', e => {
        const $button = e.target.closest(
            `.inventory__book,
                    .inventory__plus,
                    .inventory__minus`
        );

        if ($button === null) {
            return;
        }

        const $inventory = $button.closest('.inventory');
        const $count = $inventory.querySelector('.inventory__count');

        if ($button.classList.contains('inventory__book')) {
            $count.value = +$count.min + 1;
        } else {
            $count.value = +$count.value + (
                $button.classList.contains('inventory__plus')
                    ? 1
                    : -1
            );
        }

        $count.dispatchEvent(
            new Event('change', {bubbles: true})
        );
    });

    document.addEventListener('change', e => {
        const $count = e.target.closest('.inventory__count');

        if ($count === null) {
            return;
        }

        const $inventory = $count.closest('.inventory');
        const $book = $inventory.querySelector('.inventory__book');
        const $controls = $inventory.querySelector('.inventory__controls');

        if (+$count.value === 0) {
            $book.classList.remove('d-none');
            $controls.classList.add('d-none');
        } else {
            $book.classList.add('d-none');
            $controls.classList.remove('d-none');

            if (+$count.value < +$count.min) {
                $count.value = +$count.min + 1;
            } else if (+$count.value > +$count.max) {
                $count.value = +$count.max;
            }
        }

        const count = [...document.querySelectorAll('.inventory__controls:not(.d-none) .inventory__count')]
            .reduce((sum, _$count) => sum + +_$count.value, 0);

        if (count === 0) {
            $order.classList.add('opacity-0', 'pe-none');
        } else {
            $order.classList.remove('opacity-0', 'pe-none');

            $orderCount.innerText = count + ' ' + numWord(count, [
                'позицию',
                'позиции',
                'позиций'
            ]);
        }
    });

    document.addEventListener('focusin', e => {
        const $count = e.target.closest('.inventory__count');

        if ($count === null) {
            return;
        }

        $count.select();
    });

    $orderSend.addEventListener('click', async () => {
        const isAuth = $authJumbotron.classList.contains('d-none');

        if (!isAuth) {
            $modalAuth.classList.add('modal-auth_order');

            bsModalAuth.show();
        } else {
            $orderSend.disabled = true;

            const data = {};

            [...document.querySelectorAll('.inventory__controls:not(.d-none) .inventory__count')]
                .forEach($count => {
                    const $inventory = $count.closest('.inventory');

                    data[$inventory.dataset.id] = +$count.value;
                });

            const request = await fetch($orderSend.dataset.url, {
                method: 'POST',
                body: JSON.stringify(data)
            });

            window.location = await request.text();
        }
    });

    [$authNavbar, $authJumbotron].forEach($button => {
        $button.addEventListener('click', () => {
            const isAuth = $authJumbotron.classList.contains('d-none');

            if (!isAuth) {
                $modalAuth.classList.remove('modal-auth_order');

                bsModalAuth.show();
            } else {
                $authJumbotron.classList.remove('d-none');

                $authNavbar.innerText = 'Войти';
                $orderSend.innerText = 'Войти и забронировать';

                fetch($authNavbar.dataset.url,{
                    method: 'POST'
                });
            }
        });
    });

    $modalAuth.addEventListener('shown.bs.modal', () => {
        $loginLogin.focus();
    });

    $modalAuth.addEventListener('hidden.bs.modal', () => {
        $login.reset();
        $register.reset();

        $loginError.innerText = '';
        $registerError.innerText = '';

        $loginError.classList.add('d-none');
        $registerError.classList.add('d-none');

        bsModalAuthLoginTab.show();
    });

    $modalAuth.addEventListener('shown.bs.tab', e => {
        if (e.target === $modalAuthLoginTab) {
            $loginLogin.focus();
        } else {
            $registerName.focus();
        }
    });

    $modalAuth.addEventListener('submit', async e => {
        e.preventDefault();

        setModalDisabled(true);

        const formData = new FormData(e.target);

        const request = await fetch(e.target.action, {
            method: 'POST',
            body: formData,
        });

        const response = await request.text();

        if (response !== 'ok') {
            const $error = e.target === $login
                ? $loginError
                : $registerError;

            $error.innerText = response;
            $error.classList.remove('d-none');

            setModalDisabled(false);

            return;
        }

        $authJumbotron.classList.add('d-none');

        $authNavbar.innerText = 'Выйти';
        $orderSend.innerText = 'Забронировать';

        if ($modalAuth.classList.contains('modal-auth_order')) {
            $orderSend.click();
        } else {
            setModalDisabled(false);

            bsModalAuth.hide();
        }
    });
})();

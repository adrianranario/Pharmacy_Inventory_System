document.addEventListener('DOMContentLoaded', function () {
    const openButton = document.getElementById('scan-barcode-btn');
    if (!openButton) return;

    const modal = document.getElementById('scanner-modal');
    const reader = document.getElementById('barcode-reader');
    const status = document.getElementById('scanner-status');
    const textarea = document.querySelector('textarea[name="barcodes"]');

    let scanner = null;
    let scanning = false;

    function setStatus(message, isError) {
        if (!status) return;
        status.textContent = message;
        status.classList.toggle('error-text', Boolean(isError));
    }

    function appendBarcode(code) {
        if (!textarea) return;
        const codes = textarea.value.split(/[\r\n]+/).map(function (item) {
            return item.trim();
        }).filter(Boolean);

        if (codes.indexOf(code) === -1) {
            codes.push(code);
            textarea.value = codes.join('\n');
        }
        setStatus('Scanned: ' + code, false);
    }

    function stopScanner() {
        if (!scanner) return;
        const current = scanner;
        scanner = null;
        scanning = false;
        current.stop().then(function () {
            current.clear();
        }).catch(function () {
            // Camera may already be stopped.
        });
    }

    function closeModal() {
        stopScanner();
        modal.hidden = true;
        if (reader) reader.innerHTML = '';
    }

    function startScanner() {
        if (typeof Html5Qrcode === 'undefined') {
            setStatus('Scanner library failed to load. Check your internet connection.', true);
            return;
        }
        if (scanning) return;

        scanning = true;
        setStatus('Starting camera...');

        scanner = new Html5Qrcode('barcode-reader', { verbose: false });
        scanner.start(
            { facingMode: 'environment' },
            { fps: 10, qrbox: { width: 250, height: 250 } },
            function onSuccess(decodedText) {
                appendBarcode(decodedText);
                stopScanner();
                closeModal();
            },
            function onFailure() {
                // Ignore frames where no barcode was found.
            }
        ).catch(function (error) {
            scanning = false;
            const message = error && error.message ? error.message : String(error);
            setStatus('Unable to start camera: ' + message, true);
        });
    }

    openButton.addEventListener('click', function () {
        modal.hidden = false;
        startScanner();
    });

    modal.querySelectorAll('[data-close-scanner]').forEach(function (element) {
        element.addEventListener('click', closeModal);
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !modal.hidden) closeModal();
    });
});

export function get_csrf_token() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
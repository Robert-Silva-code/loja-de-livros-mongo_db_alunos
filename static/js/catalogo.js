document.addEventListener('DOMContentLoaded', function() {
    // Seleção dinâmica de tags de categoria (feedback visual ao clicar)
    document.querySelectorAll('.tag-category').forEach(tag => {
        tag.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input[type="checkbox"]');
            input.checked = !input.checked;
            this.classList.toggle('ring-2');
            this.classList.toggle('ring-orange-500');
            this.classList.toggle('bg-orange-100');
            this.classList.toggle('dark:bg-orange-800');
            this.classList.toggle('text-orange-700');
            this.classList.toggle('dark:text-orange-200');
            this.classList.toggle('border-orange-400');
            this.classList.toggle('dark:border-orange-600');
        });
    });

    // Redirecionamento ao clicar no card do livro
    document.querySelectorAll('[data-id]').forEach(card => {
        card.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            if (id) window.location.href = '/livro/' + id;
        });
    });

    // tags gerenciamento
    document.querySelectorAll('.tag-row').forEach(function(row) {
        const include = row.querySelector('.tag-include');
        const exclude = row.querySelector('.tag-exclude');
        const includeIcon = row.querySelector('.include-icon');
        const excludeIcon = row.querySelector('.exclude-icon');
        const includeLabel = row.querySelector('label:first-child');
        const excludeLabel = row.querySelector('label:last-child');

        function updateSelection() {
            // Limpa destaque e ícones
            row.classList.remove(
                'bg-green-100', 'dark:bg-green-800', 'ring-2', 'ring-green-500',
                'bg-red-100', 'dark:bg-red-800', 'ring-red-500'
            );
            includeIcon.classList.add('hidden');
            excludeIcon.classList.add('hidden');

            // Incluir (verde)
            if (include.checked) {
                row.classList.add('bg-green-100', 'dark:bg-green-800', 'ring-2', 'ring-green-500');
                includeIcon.classList.remove('hidden');
                exclude.checked = false;
            }
            // Excluir (vermelho)
            else if (exclude.checked) {
                row.classList.add('bg-red-100', 'dark:bg-red-800', 'ring-2', 'ring-red-500');
                excludeIcon.classList.remove('hidden');
                include.checked = false;
            }
        }

        // Alterna ao clicar no label do verde (ícone/incluir)
        includeLabel.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (include.checked) {
                include.checked = false;
            } else {
                include.checked = true;
                exclude.checked = false;
            }
            updateSelection();
        });

        // Alterna ao clicar no label do vermelho (ícone/excluir)
        excludeLabel.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (exclude.checked) {
                exclude.checked = false;
            } else {
                exclude.checked = true;
                include.checked = false;
            }
            updateSelection();
        });

        // Alterna ao clicar na linha (opcional, pode remover se não quiser)
        row.addEventListener('click', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.closest('label')) return;
            if (!include.checked && !exclude.checked) {
                include.checked = true;
            } else if (include.checked) {
                include.checked = false;
            } else if (exclude.checked) {
                exclude.checked = false;
            }
            updateSelection();
        });

        // Inicializa estado visual
        updateSelection();
    });

    // Clique no card do livro (mantém do seu catálogo)
    document.querySelectorAll('[data-id]').forEach(card => {
        card.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            if (id) window.location.href = '/livro/' + id;
        });
    });
});

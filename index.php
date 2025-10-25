<?php include('header.php'); ?>

<main class="container my-5 flex-grow-1">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <h2 class="card-title text-center mb-4">Descubra seu signo</h2>
                    <p class="text-center text-muted">Insira sua data de nascimento abaixo para saber mais sobre seu signo zodiacal.</p>
                    
                    <!-- Formulário que envia os dados para show_zodiac_sign.php -->
                    <form id="signo-form" method="POST" action="show_zodiac_sign.php">
                        <div class="mb-3">
                            <label for="data_nascimento" class="form-label">Data de Nascimento:</label>
                            <input type="date" class="form-control" id="data_nascimento" name="data_nascimento" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">Descobrir!</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</main>

<footer class="mt-auto bg-dark text-white text-center p-3">
    <p class="mb-0">Desenvolvido como atividade prática.</p>
</footer>

<!-- Bootstrap JS (Opcional, mas bom para componentes interativos) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
</body>
</html>

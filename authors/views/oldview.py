@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()
    #  O filter retorna um QuerySet. Logo, precisamos
    #  colocar .first() para retornar o primeiro encontrado

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        #  Bound Form(Quando tem dados) or None
        data=request.POST or None,
        files=request.FILES or None,
        #  Vinculado ao recipe
        instance=recipe,
    )

    if form.is_valid():
        #  Agora, o form é válido e eu posso tentar salvar
        recipe = form.save(commit=False)

        # Passando todas as informações que o usuário não editou como hard coded # noqa: E501
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        {
            'form': form
        })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None
    )

    if request.POST:
        if form.is_valid():
            new_recipe = form.save(commit=False)

            new_recipe.author = request.user
            new_recipe.preparation_steps_is_html = False
            new_recipe.is_published = False

            new_recipe.save()

            messages.success(request, 'Receita criada com sucesso')
            return redirect(reverse('authors:dashboard'))  # noqa: E501

    return render(
        request,
        'authors/pages/dashboard_recipe_new.html',
        {
            'form': form,
        }
    )

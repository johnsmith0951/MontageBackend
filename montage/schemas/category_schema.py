from accounts.models import MontageUser
from portraits.models import (Question, Impression)
from categories.models import Category
from django.forms import ModelForm
from django.forms import ValidationError

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.forms.mutation import DjangoFormMutation


class CreateCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description',)


class CategoryType(DjangoObjectType):
    """CategoryType"""
    class Meta:
        """Meta."""
        model = Category


class CreateCategoryMutation(DjangoModelFormMutation):
    """
    カテゴリの作成

    IN
    ====
    mutation {
      createCategory(input:{
         name: "お買い物",
         description: "ショッピング情報について全般"
         })
      {
        category{
          name
          description
        }
      }
    }
    """
    class Meta:
        form_class = CreateCategoryForm


class UpdateCategoryMutation(graphene.Mutation):
    """
    カテゴリの更新

    """
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        description = graphene.String()

    def mutate(self, info, id, name, description):
        cat = Category.objects.get(id=id)
        cat.name = name
        cat.description = description
        cat.save()

        return UpdateCategoryMutation(id=id, name=name, description=description)


class DeleteCategoryMutation(graphene.Mutation):
    """
    カテゴリの削除

    IN
    ====
    mutation {
      deleteCategory(id: 3){
        id
      }
    }
    """
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        Category.objects.filter(id=id).delete()
        return DeleteCategoryMutation(id=id)


class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


class Query(graphene.ObjectType):
    category = graphene.Field(CategoryType, name=graphene.String())
    categories = graphene.List(CategoryType)

    def resolve_category(self, name, info):
        return Category.objects.get(name=name)

    def resolve_categories(self, info):
        return Category.objects.all()

<script>
    import CharField from './fields/CharField.svelte'
    import BooleanField from './fields/BooleanField.svelte'
    import TextField from './fields/TextField.svelte'
    import IntegerField from './fields/IntegerField.svelte'
    import FloatField from './fields/FloatField.svelte'
    import ForeignKeyField from './fields/ForeignKeyField.svelte'
    import DateField from './fields/DateField.svelte'
    import SelectField from './fields/SelectField.svelte'
    import ManyToManyField from './fields/ManyToManyField.svelte'
    import BackRefField from './fields/BackRefField.svelte'
    import FileField from './fields/FileField.svelte'
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    export let type;
    export let label;
    export let value;
    export let edit;
    export let password;
    export let model;
    export let filters = [];
    export let options = [];
    export let required;
    export let relatedFields;
    export let relatedFieldsDesc;
    export let nolabel;
    export let add;
    export let remove;
    export let readonly;

    function changed(){
        dispatch("change", {});
    }

    function getClass(){
        let classes = ["field"];
        if(required){
            classes.push("required");
        }
        if(nolabel){
            classes.push("nolabel");
        }
        return classes.join(" ");
    }
</script>

<div class={getClass()}>
    {#if type}
        {#if type === "char"}
            <CharField
                label={label}
                bind:value={value}
                edit={edit}
                password={password}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "boolean"}
            <BooleanField
                label={label}
                bind:value={value}
                edit={edit}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "text"}
            <TextField
                label={label}
                bind:value={value}
                edit={edit}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "integer"}
            <IntegerField
                label={label}
                bind:value={value}
                edit={edit}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "float"}
            <FloatField
                label={label}
                bind:value={value}
                edit={edit}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "foreignkey" }
            <ForeignKeyField
                label={label}
                bind:value={value}
                edit={edit}
                model={model}
                filters={filters}
                on:change={changed}
                query={value?value.name:''}
                readonly={readonly}
            />
        {:else if type === "date"}
            <DateField
                label={label}
                bind:value={value}
                edit={edit}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "select"}
            <SelectField
                label={label}
                bind:value={value}
                edit={edit}
                options={options}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "manytomany"}
            <ManyToManyField
                label={label}
                bind:value={value}
                edit={edit}
                model={model}
                filters={filters}
                relatedFields={relatedFields}
                relatedFieldsDesc={relatedFieldsDesc}
                allowAdd={add}
                allowRemove={remove}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "backref"}
            <BackRefField
                label={label}
                bind:value={value}
                edit={edit}
                model={model}
                filters={filters}
                relatedFields={relatedFields}
                relatedFieldsDesc={relatedFieldsDesc}
                allowAdd={add}
                allowRemove={remove}
                on:change={changed}
                readonly={readonly}
            />
        {:else if type === "file"}
            <FileField
                label={label}
                bind:value={value}
                edit={edit}
                on:change={changed}
                readonly={readonly}
            />
        {/if}
    {/if}
</div>

<style>
    .required :global(label::after){
        content:"*";
        color:red
    }
    .required :global(input, select){
        background-color:seashell
    }
    .nolabel :global(label){
        display: none
    }

</style>
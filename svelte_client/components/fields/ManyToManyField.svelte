<script>
    import ForeignKeyField from './ForeignKeyField.svelte';
    import { call } from "../../services/service.js"
    export let label = "";
    export let model = "";
    export let filters = [];
    export let value = [];
    export let edit;
    export let relatedFields = [];
    export let relatedFieldsDesc = {};
    export let allowAdd;
    export let allowRemove;
    export let readonly;
    let valueFK;

    function renderField(obj, field){
        let val = obj[field];
        if(typeof(val) == "number" || typeof(val) == "string"){
            return val;
        }else if(typeof(val) === "object"){
            return val.name || val.id;
        }else{
            return val;
        }

    }

    function add(event){
        if(!event.detail.id){
            return;
        }
        let ids = [];
        for(let obj of value){
            ids.push(obj.id);
        }
        if(!ids.includes(event.detail.id)){
            value.push(event.detail);
            value = value;
        }
    }

    function remove(id){
        for(let i=0;i<value.length;i++){
            if(value[i].id==id){
                value.splice(i,1);
                value = value;
                break;
            }
        }
    }
</script>

<div class="form-group">
    <label>{label}</label>
    {#if edit && allowAdd && !readonly}
        <ForeignKeyField
            label=""
            bind:value={valueFK}
            edit={edit}
            model={model}
            filters={filters}
            on:change={add}
            relatedFields={relatedFields}
            placeholder="Agregar elemento"
        />
    {/if}
    <table class="table table-sm">
        <thead class="thead-light">
            <tr>
                {#each relatedFields as field}
                    {#if !relatedFieldsDesc || !relatedFieldsDesc[field.field]}
                        <th>{field.field}</th>
                    {:else}
                        <th>{relatedFieldsDesc[field.field].label}</th>
                    {/if}
                {/each}
                <th></th>
            </tr>
        </thead>
        {#if (value || []).length>0}
            {#each value as obj}
                <tr>
                    {#each relatedFields as field}
                        <td>{renderField(obj, field.field)}</td>
                    {/each}
                    <td class="basura">
                        {#if allowRemove}
                            <img
                                hidden={!edit}
                                on:click={()=>remove(obj.id)}
                                src="icons/trash-fill.svg"
                                alt="Remover"/>
                        {/if}
                    </td>
                </tr>
            {/each}
        {:else}
            <tr>
                <td colspan="100">(Sin elementos)</td>
            </tr>
        {/if}
    </table>
</div>

<style>
    table{
        border: 1px solid silver;
        background-color: white;
    }
    .basura{
        text-align:right;
        cursor: pointer;
    }
</style>
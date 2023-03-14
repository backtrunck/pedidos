drop table if exists pedidos.item_pedido;
drop table if exists pedidos.produto;
drop table if exists pedidos.categoria;
drop table if exists pedidos.pedido;
drop table if exists pedidos.cliente;

create table pedidos.cliente(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cpf CHAR(11) NOT NULL UNIQUE,
    nm_cliente VARCHAR(200)
);
    
create table pedidos.categoria(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ds_categoria VARCHAR(100) NOT NULL 
);

CREATE TABLE pedidos.produto(
	id INT NOT NULL AUTO_INCREMENT primary key,
    cod_barras CHAR(15) NOT NULL, 
    ds_produto VARCHAR(200) NOT NULL, 
    categoria_id INT NOT NULL,
    constraint fk_categoria_id foreign key idx_categoria_id(categoria_id) references categoria(id)
);

CREATE TABLE pedidos.pedido(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dt_pedido DATE NOT NULL DEFAULT(CURRENT_DATE),
    cliente_id INT NOT NULL,
    constraint fk_cliente_id foreign key idx_cliente_id(cliente_id) references cliente(id)
);

create table pedidos.item_pedido(
	pedido_id INT NOT NULL,
    produto_id INT NOT NULL,
    vl_item DECIMAL(9,2) NOT NULL,
    primary key(pedido_id, produto_id),
    constraint fk_pedido_id foreign key idx_pedido_id(pedido_id) references pedido(id),
    constraint fk_produto_id foreign key idx_produto_id(produto_id) references produto(id)
);
